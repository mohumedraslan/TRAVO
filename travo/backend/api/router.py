from fastapi import APIRouter

# Import service routers
from services.user_service.routes import router as user_router
from services.recommendation_service.routes import router as recommendation_router
from services.crowd_service.routes import router as crowd_router
from services.vision_service.routes import router as vision_router
from services.assistant_service.routes import router as assistant_router
from services.business_service.routes import router as business_router

# Create main API router
api_router = APIRouter()

# Include all service routers
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(recommendation_router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(crowd_router, prefix="/crowds", tags=["crowds"])
api_router.include_router(vision_router, prefix="/vision", tags=["vision"])
api_router.include_router(assistant_router, prefix="/assistant", tags=["assistant"])
api_router.include_router(business_router, prefix="/business", tags=["business"])
