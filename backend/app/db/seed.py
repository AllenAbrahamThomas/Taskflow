import sys
import os
from sqlalchemy.orm import Session

# Add the project root to path so we can run the seed script directly
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def seed_db(db: Session):
    print("Seeding database...")
    
    # 1. Seed Admin User
    admin_email = "admin@taskflow.com"
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        admin_user = User(
            name="System Admin",
            email=admin_email,
            password_hash=get_password_hash("AdminPass123!"),
            role="admin"
        )
        db.add(admin_user)
        print(f"Created admin user: {admin_email}")
    else:
        print(f"Admin user already exists: {admin_email}")
        
    # 2. Seed Developer User
    dev_email = "dev@taskflow.com"
    dev_user = db.query(User).filter(User.email == dev_email).first()
    if not dev_user:
        dev_user = User(
            name="Jane Developer",
            email=dev_email,
            password_hash=get_password_hash("DevPass123!"),
            role="developer"
        )
        db.add(dev_user)
        print(f"Created developer user: {dev_email}")
    else:
        print(f"Developer user already exists: {dev_email}")
        
    db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
