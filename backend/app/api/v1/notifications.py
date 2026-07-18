import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.notification import (
    Notification,
    NotificationType,
    NotificationStatus,
    DeviceToken,
)
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.notification import (
    SendNotificationRequest,
    NotificationResponse,
    PaginatedNotifications,
    DeviceTokenRequest,
    DeviceTokenResponse,
)
from app.services.fcm import FCMService

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/notifications", tags=["Notifications"])

ALLOWED_SORT_FIELDS = ["id", "notification_type", "status", "created_at", "sent_at"]


@router.post(
    "/send",
    response_model=list[NotificationResponse],
    summary="Send push notification",
    description=(
        "Send a push notification to one or more pilgrims via FCM. "
        "If pilgrim_ids is empty or null, broadcasts to all active pilgrims."
    ),
    responses={
        200: {"description": "Notification(s) created and delivery attempted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def send_notification(
    body: SendNotificationRequest,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    fcm = FCMService()
    is_broadcast = not body.pilgrim_ids

    if is_broadcast:
        pilgrims = db.query(User).filter(User.role == Role.pilgrim, User.is_active == True).all()
        target_ids = [p.id for p in pilgrims]
    else:
        target_ids = body.pilgrim_ids

    if target_ids:
        tokens = (
            db.query(DeviceToken)
            .filter(
                DeviceToken.pilgrim_id.in_(target_ids),
                DeviceToken.is_active == True,
            )
            .all()
        )
    else:
        tokens = []

    if not tokens:
        notification = Notification(
            title=body.title,
            body=body.body,
            notification_type=body.notification_type,
            pilgrim_id=target_ids[0] if len(target_ids) == 1 else None,
            is_broadcast=is_broadcast,
            status=NotificationStatus.pending,
            fcm_response="No device tokens found",
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return [NotificationResponse.model_validate(notification)]

    token_list = [t.token for t in tokens]
    token_pilgrim_map = {t.token: t.pilgrim_id for t in tokens}

    notifications = []
    if fcm.is_configured():
        results = fcm.send_to_tokens(
            token_list,
            body.title,
            body.body,
            data={"type": body.notification_type.value},
        )
        for r in results:
            n = Notification(
                title=body.title,
                body=body.body,
                notification_type=body.notification_type,
                pilgrim_id=token_pilgrim_map.get(r["token"]),
                is_broadcast=is_broadcast,
                status=NotificationStatus.sent if r["success"] else NotificationStatus.failed,
                fcm_response=str(r.get("response", r.get("error", ""))),
                sent_at=datetime.utcnow() if r["success"] else None,
            )
            db.add(n)
            notifications.append(n)
    else:
        for token in token_list:
            n = Notification(
                title=body.title,
                body=body.body,
                notification_type=body.notification_type,
                pilgrim_id=token_pilgrim_map.get(token),
                is_broadcast=is_broadcast,
                status=NotificationStatus.pending,
                fcm_response="FCM not configured",
            )
            db.add(n)
            notifications.append(n)

    db.commit()
    for n in notifications:
        db.refresh(n)

    return [NotificationResponse.model_validate(n) for n in notifications]


@router.get(
    "",
    response_model=PaginatedNotifications,
    summary="List notification history",
    description="Retrieve a paginated list of sent notifications. Supports search, sorting, and filtering by type and status.",
    responses={
        200: {"description": "Paginated notification history"},
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
):
    query = db.query(Notification)

    if notification_type:
        query = query.filter(Notification.notification_type == notification_type)

    if status_filter:
        query = query.filter(Notification.status == status_filter)

    query = sorting.apply(query, Notification, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    return PaginatedNotifications(
        items=[NotificationResponse.model_validate(n) for n in result["items"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"],
    )


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
