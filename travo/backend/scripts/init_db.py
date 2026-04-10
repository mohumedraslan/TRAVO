"""
Database initialization script for TRAVO
Creates all necessary tables and initial data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, inspect
from services.user_service.models import Base as UserBase, User, UserPreferences
from services.user_service.database import engine, SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize database tables"""
    try:
        logger.info("Starting database initialization...")
        
        # Create all tables
        logger.info("Creating tables...")
        UserBase.metadata.create_all(bind=engine)
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {tables}")
        
        # Check if users table exists
        if 'users' in tables:
            logger.info("✅ Users table created successfully")
        else:
            logger.error("❌ Users table was not created")
            return False
            
        if 'user_preferences' in tables:
            logger.info("✅ User preferences table created successfully")
        else:
            logger.error("❌ User preferences table was not created")
            return False
        
        # Create a test user if none exists
        db = SessionLocal()
        try:
            existing_user = db.query(User).filter(User.email == "test@travo.com").first()
            if not existing_user:
                # Use simple hash for test user
                import hashlib
                simple_hash = hashlib.sha256("testpass123".encode()).hexdigest()
                
                test_user = User(
                    email="test@travo.com",
                    name="Test User",
                    password_hash=simple_hash
                )
                db.add(test_user)
                db.commit()
                db.refresh(test_user)
                logger.info(f"✅ Created test user: test@travo.com / testpass123")
                
                # Create preferences for test user
                test_prefs = UserPreferences(
                    user_id=test_user.id,
                    interests='["Cultural", "Historical"]',
                    preferred_cities='["Cairo", "Luxor"]',
                    saved_itineraries='[]',
                    preferred_language="en"
                )
                db.add(test_prefs)
                db.commit()
                logger.info(f"✅ Created preferences for test user")
            else:
                logger.info(f"Test user already exists: {existing_user.email}")
        finally:
            db.close()
        
        logger.info("✅ Database initialization complete!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
