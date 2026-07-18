import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, Role


def seed():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@hajj.ng").first()
        if admin:
            print("Admin user already exists.")
            return

        admin = User(
            email="admin@hajj.ng",
            full_name="System Admin",
            hashed_password=hash_password("admin123"),
            role=Role.admin,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print("Admin user created: admin@hajj.ng / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
