from app.db.models import User
from app.core.security import hash_password


def create_admin(db):
    admin = db.query(User).filter(User.email == "admin@omnibioai").first()

    if not admin:
        admin = User(
            email="admin@omnibioai",
            hashed_password=hash_password("admin"),
            status="active"
        )

        db.add(admin)
        db.commit()