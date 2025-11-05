from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from config import settings

# Import the main API router
from api.router import api_router
from services.vision_service.service_logic import load_identification_model, load_detection_model

# Socket.IO for real-time communication
import socketio
from services.assistant_service.service_logic import get_ai_response

# Create FastAPI app
app = FastAPI(
    title="TRAVO API",
    description="AI-Powered Travel Companion API",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8081",
    # Add your production frontend URL here
    # "https://your-frontend-domain.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Loading ML models...")
    load_identification_model()
    load_detection_model()
    print("ML models loaded successfully.")

# Include the main API router
app.include_router(api_router, prefix="/api")

# Mount static files directory for docs
docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
app.mount("/static", StaticFiles(directory=docs_dir), name="static")

# Initialize Socket.IO server and mount under /socket.io
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app.mount("/socket.io", socketio.ASGIApp(sio))

# Socket.IO event handlers
@sio.event
async def connect(sid, environ, auth):
    # Simple connect log, could be extended with auth
    print(f"Socket connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Socket disconnected: {sid}")

@sio.event
async def assistant_query(sid, data):
    """
    Handle assistant queries over Socket.IO.
    Expects data: {"query": str, "location": Optional[str]}
    Emits: 'assistant_response' with {"answer": str, "confidence": float, "related_monuments": list}
    """
    try:
        query = data.get("query")
        location = data.get("location")
        if not query:
            await sio.emit("assistant_response", {"answer": "No query provided."}, to=sid)
            return
        result = get_ai_response(query, location)
        payload = {
            "answer": result.get("answer", ""),
            "confidence": result.get("confidence", 0.0),
            "related_monuments": result.get("related_monuments", []),
        }
        await sio.emit("assistant_response", payload, to=sid)
    except Exception as e:
        print(f"Error in assistant_query: {e}") # Log the full error for debugging
        await sio.emit("assistant_response", {"answer": "An unexpected error occurred."}, to=sid)

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
    uvicorn.run("main:app", host="0.0.0.0", port=settings.API_PORT, reload=True)
