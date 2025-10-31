from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# Import the main API router
from api.router import api_router

# Create FastAPI app
app = FastAPI(
    title="TRAVO API",
    description="AI-Powered Travel Companion API",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main API router
app.include_router(api_router, prefix="/api")

# Mount static files directory for docs
docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
app.mount("/static", StaticFiles(directory=docs_dir), name="static")

# API Spec endpoint
@app.get("/api_spec.yaml")
async def get_api_spec():
    api_spec_path = os.path.join(docs_dir, "api_spec.yaml")
    return FileResponse(api_spec_path)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to TRAVO API",
        "docs": "/docs",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
