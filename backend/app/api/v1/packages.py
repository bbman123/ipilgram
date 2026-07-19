from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.package import Package
from app.models.flight import Flight
from app.models.accommodation import Accommodation
from app.models.transport import Transport
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.response import success_response
from app.schemas.package import (
    PackageCreate,
    PackageUpdate,
    PackageResponse,
    PackageDetailResponse,
    PaginatedPackages,
)
from app.schemas.pilgrim import PilgrimResponse, PaginatedPilgrims

router = APIRouter(prefix="/packages", tags=["Packages"])

ALLOWED_SORT_FIELDS = ["id", "name", "created_at"]


def _enrich_package(pkg: Package, pilgrim_counts: dict[int, int]) -> PackageResponse:
    return PackageResponse(
        id=pkg.id,
        name=pkg.name,
        description=pkg.description,
        flight_id=pkg.flight_id,
        accommodation_id=pkg.accommodation_id,
        transport_id=pkg.transport_id,
        pilgrim_count=pilgrim_counts.get(pkg.id, 0),
        created_at=pkg.created_at,
        updated_at=pkg.updated_at,
    )


@router.get(
    "",
    summary="List all packages",
    description="Retrieve a paginated list of Hajj packages. Supports search and sorting.",
    responses={
        200: {"description": "Paginated list of packages"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_packages(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    search: str = Query("", max_length=255, description="Search by package name"),
):
    query = db.query(Package)

    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Package.name.ilike(pattern)))

    query = sorting.apply(query, Package, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    package_ids = [p.id for p in result["items"]]
    counts = {}
    if package_ids:
        rows = (
            db.query(User.package_id, func.count(User.id))
            .filter(User.package_id.in_(package_ids), User.role == Role.pilgrim)
            .group_by(User.package_id)
            .all()
        )
        counts = {row[0]: row[1] for row in rows}

    return success_response(
        data=PaginatedPackages(
            items=[_enrich_package(p, counts) for p in result["items"]],
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"],
        ).model_dump(),
        message="Packages retrieved successfully",
    )


@router.get(
    "/{package_id}",
    summary="Get package by ID",
    description="Retrieve a single package with its associated flight, accommodation, and transport details.",
    responses={
        200: {"description": "Package with full details"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Package not found"},
    },
)
def get_package(
    package_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
        )

    flight = db.query(Flight).filter(Flight.id == pkg.flight_id).first() if pkg.flight_id else None
    accommodation = db.query(Accommodation).filter(Accommodation.id == pkg.accommodation_id).first() if pkg.accommodation_id else None
    transport = db.query(Transport).filter(Transport.id == pkg.transport_id).first() if pkg.transport_id else None
    pilgrim_count = db.query(func.count(User.id)).filter(User.package_id == pkg.id, User.role == Role.pilgrim).scalar()

    return success_response(
        data=PackageDetailResponse(
            id=pkg.id,
            name=pkg.name,
            description=pkg.description,
            flight=flight,
            accommodation=accommodation,
            transport=transport,
            pilgrim_count=pilgrim_count,
            created_at=pkg.created_at,
            updated_at=pkg.updated_at,
        ).model_dump(),
        message="Package retrieved successfully",
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new package",
    description="Create a new Hajj package with optional flight, accommodation, and transport associations.",
    responses={
        201: {"description": "Package created successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Referenced flight, accommodation, or transport not found"},
    },
)
def create_package(
    body: PackageCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    if body.flight_id:
        if not db.query(Flight).filter(Flight.id == body.flight_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    if body.accommodation_id:
        if not db.query(Accommodation).filter(Accommodation.id == body.accommodation_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accommodation not found")
    if body.transport_id:
        if not db.query(Transport).filter(Transport.id == body.transport_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transport not found")

    pkg = Package(**body.model_dump())
    db.add(pkg)
    db.commit()
    db.refresh(pkg)
    return success_response(data=PackageResponse.model_validate(pkg).model_dump(), message="Package created successfully")


@router.put(
    "/{package_id}",
    summary="Update package details",
    description="Update an existing package. Only provided fields are modified.",
    responses={
        200: {"description": "Package updated successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Package not found"},
    },
)
def update_package(
    package_id: int,
    body: PackageUpdate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
        )

    update_data = body.model_dump(exclude_unset=True)

    if "flight_id" in update_data and update_data["flight_id"]:
        if not db.query(Flight).filter(Flight.id == update_data["flight_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    if "accommodation_id" in update_data and update_data["accommodation_id"]:
        if not db.query(Accommodation).filter(Accommodation.id == update_data["accommodation_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accommodation not found")
    if "transport_id" in update_data and update_data["transport_id"]:
        if not db.query(Transport).filter(Transport.id == update_data["transport_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transport not found")

    for field, value in update_data.items():
        setattr(pkg, field, value)

    db.commit()
    db.refresh(pkg)

    pilgrim_count = db.query(func.count(User.id)).filter(User.package_id == pkg.id, User.role == Role.pilgrim).scalar()
    return success_response(
        data=PackageResponse(
            id=pkg.id,
            name=pkg.name,
            description=pkg.description,
            flight_id=pkg.flight_id,
            accommodation_id=pkg.accommodation_id,
            transport_id=pkg.transport_id,
            pilgrim_count=pilgrim_count,
            created_at=pkg.created_at,
            updated_at=pkg.updated_at,
        ).model_dump(),
        message="Package updated successfully",
    )


class AssignPackageResponse(PackageResponse):
    pass


@router.post(
    "/{package_id}/assign/{pilgrim_id}",
    status_code=status.HTTP_200_OK,
    summary="Assign package to pilgrim",
    description="Assign a package to a pilgrim. The pilgrim inherits the associated flight, accommodation, and transport.",
    responses={
        200: {"description": "Package assigned successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Package or pilgrim not found"},
    },
)
def assign_package(
    package_id: int,
    pilgrim_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")

    pilgrim = db.query(User).filter(User.id == pilgrim_id, User.role == Role.pilgrim).first()
    if not pilgrim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pilgrim not found")

    pilgrim.package_id = package_id
    db.commit()

    pilgrim_count = db.query(func.count(User.id)).filter(User.package_id == pkg.id, User.role == Role.pilgrim).scalar()
    return success_response(
        data=PackageResponse(
            id=pkg.id,
            name=pkg.name,
            description=pkg.description,
            flight_id=pkg.flight_id,
            accommodation_id=pkg.accommodation_id,
            transport_id=pkg.transport_id,
            pilgrim_count=pilgrim_count,
            created_at=pkg.created_at,
            updated_at=pkg.updated_at,
        ).model_dump(),
        message="Package assigned successfully",
    )


@router.get(
    "/{package_id}/pilgrims",
    summary="List pilgrims assigned to a package",
    description="Retrieve a paginated list of pilgrims assigned to a specific package. Supports search and pagination.",
    responses={
        200: {"description": "Paginated list of pilgrims in this package"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Package not found"},
    },
)
def list_package_pilgrims(
    package_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    search: str = Query("", max_length=255, description="Search by name, email, or phone"),
):
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
        )

    query = db.query(User).filter(User.role == Role.pilgrim, User.package_id == package_id)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                User.full_name.ilike(pattern),
                User.email.ilike(pattern),
                User.phone.ilike(pattern),
            )
        )

    query = query.order_by(User.full_name.asc())
    result = paginate(query, pagination)

    items = []
    for u in result["items"]:
        resp = PilgrimResponse.model_validate(u)
        resp.package_name = pkg.name
        items.append(resp)

    return success_response(
        data=PaginatedPilgrims(
            items=items,
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"],
        ).model_dump(),
        message="Package pilgrims retrieved successfully",
    )


@router.delete(
    "/{package_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a package",
    description="Permanently remove a package record. Assigned pilgrims will be unlinked.",
    responses={
        204: {"description": "Package deleted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Package not found"},
    },
)
def delete_package(
    package_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
        )
    db.query(User).filter(User.package_id == package_id).update({"package_id": None})
    db.delete(pkg)
    db.commit()
