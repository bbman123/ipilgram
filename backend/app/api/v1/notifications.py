import logging
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_role, get_current_user
from app.models.user import User, Role
from app.models.notification import (
    Notification,
    NotificationType,
    NotificationStatus,
    DeviceToken,
)
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.notification import (
    NotificationResponse,
    PaginatedNotifications,
    DeviceTokenRequest,
    DeviceTokenResponse,
)
from app.services.fcm import FCMService

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/notifications", tags=["Notifications"])

ALLOWED_SORT_FIELDS = ["id", "notification_type", "status", "created_at", "sent_at", "scheduled_time"]


@router.get(
    "",
    response_model=PaginatedNotifications,
    summary="List all notifications (admin)",
    description="Admin endpoint. Retrieve a paginated list of all notifications across all pilgrims. Supports filtering by type and status.",
    responses={
        200: {"description": "Paginated notification list"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_notifications(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    notification_type: NotificationType | None = Query(None, alias="type", description="Filter by notification type"),
    status_filter: NotificationStatus | None = Query(None, alias="status", description="Filter by delivery status"),
    pilgrim_id: int | None = Query(None, description="Filter by pilgrim ID"),
):
    query = db.query(Notification)

    if notification_type:
        query = query.filter(Notification.notification_type == notification_type)
    if status_filter:
        query = query.filter(Notification.status == status_filter)
    if pilgrim_id:
        query = query.filter(Notification.pilgrim_id == pilgrim_id)

    query = sorting.apply(query, Notification, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    return PaginatedNotifications(
        items=[NotificationResponse.model_validate(n) for n in result["items"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"],
    )


@router.get(
    "/my",
    response_model=list[NotificationResponse],
    summary="Get my notifications (pilgrim)",
    description="Pilgrim endpoint. Retrieve all notifications for the authenticated pilgrim, ordered by scheduled_time.",
    responses={
        200: {"description": "List of notifications for the pilgrim"},
        401: {"description": "Authentication required"},
        403: {"description": "Pilgrim role required"},
    },
)
def get_my_notifications(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(Role.pilgrim))],
):
    notifications = (
        db.query(Notification)
        .filter(Notification.pilgrim_id == current_user.id)
        .order_by(Notification.scheduled_time.desc().nullslast(), Notification.created_at.desc())
        .limit(50)
        .all()
    )
    return [NotificationResponse.model_validate(n) for n in notifications]


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Mark notification as read",
    description="Mark a single notification as read by setting read_at and status to 'read'.",
    responses={
        200: {"description": "Notification marked as read"},
        401: {"description": "Authentication required"},
        403: {"description": "Can only mark your own notifications"},
        404: {"description": "Notification not found"},
    },
)
def mark_notification_read(
    notification_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    n = db.query(Notification).filter(Notification.id == notification_id).first()
    if not n:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    if n.pilgrim_id != current_user.id and current_user.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your notification")

    n.read_at = datetime.now(timezone.utc)
    n.status = NotificationStatus.read
    db.commit()
    db.refresh(n)
    return NotificationResponse.model_validate(n)


@router.post(
    "/devices",
    response_model=DeviceTokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register device token",
    description=(
        "Register an FCM/APNs device token for push notification delivery. "
        "If the token already exists, reactivates it and updates the platform."
    ),
    responses={
        201: {"description": "Device token registered"},
        401: {"description": "Authentication required"},
    },
)
def register_device(
    body: DeviceTokenRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(Role.admin, Role.pilgrim))],
):
    existing = db.query(DeviceToken).filter(DeviceToken.token == body.token).first()
    if existing:
        existing.is_active = True
        existing.platform = body.platform
        db.commit()
        db.refresh(existing)
        return DeviceTokenResponse.model_validate(existing)

    dt = DeviceToken(
        pilgrim_id=current_user.id,
        token=body.token,
        platform=body.platform,
    )
    db.add(dt)
    db.commit()
    db.refresh(dt)
    return DeviceTokenResponse.model_validate(dt)


@router.delete(
    "/devices/{token_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deactivate device token",
    description="Soft-delete a device token to stop receiving push notifications on that device.",
    responses={
        204: {"description": "Device token deactivated"},
        401: {"description": "Authentication required"},
        403: {"description": "Can only deactivate your own tokens"},
        404: {"description": "Device token not found"},
    },
)
def unregister_device(
    token_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(Role.pilgrim))],
):
    dt = db.query(DeviceToken).filter(
        DeviceToken.id == token_id,
        DeviceToken.pilgrim_id == current_user.id,
    ).first()
    if not dt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device token not found")
    dt.is_active = False
    db.commit()
