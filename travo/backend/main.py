import sys
if sys.platform == 'win32':
    # This is a workaround for a known issue with torchaudio on Windows
    # where it fails to find the FFmpeg DLLs.
    # See: https://github.com/pytorch/audio/issues/3789
    try:
        from torchaudio._extension.utils import _init_dll_path
        _init_dll_path()
    except ImportError:
        # torchaudio is optional, skip if not installed
        pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("travo_backend.log"),
        logging.StreamHandler()
    ]
)
logging.getLogger('numba').setLevel(logging.WARNING)

# Load environment variables early
load_dotenv('config.env')

# Import the main API router
from api.router import api_router

# Socket.IO for real-time communication
import socketio
# External AI models are disabled; assistant uses static descriptions only

# Initialize database
from services.user_service.database import init_db
init_db()

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

# Mount assets directory to serve images from repository data folder
# Try repo root: ../../.. -> /data, then /travo/data, then backend/data
_here = os.path.abspath(__file__)
_travo_dir = os.path.dirname(os.path.dirname(_here))
_repo_root = os.path.dirname(_travo_dir)
assets_dir_root = os.path.join(_repo_root, "data")
assets_dir_travo = os.path.join(_travo_dir, "data")
assets_dir_backend = os.path.join(os.path.dirname(_here), "data")
if os.path.isdir(assets_dir_root):
    app.mount("/assets", StaticFiles(directory=assets_dir_root), name="assets")
elif os.path.isdir(assets_dir_travo):
    app.mount("/assets", StaticFiles(directory=assets_dir_travo), name="assets")
elif os.path.isdir(assets_dir_backend):
    app.mount("/assets", StaticFiles(directory=assets_dir_backend), name="assets")

# Initialize Socket.IO server and mount under /socket.io
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app.mount("/socket.io", socketio.ASGIApp(sio))

# Socket.IO event handlers
@sio.event
async def connect(sid, environ, auth):
    # Simple connect log, could be extended with auth
    logging.info(f"Socket connected: {sid}")

@sio.event
async def disconnect(sid):
    logging.info(f"Socket disconnected: {sid}")

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
        # Static description-based response using local data only
        answer = None
        model_used = None

        if not answer:
            try:
                data_path = os.path.join(os.path.dirname(__file__), "data", "monuments.json")
                catalog = []
                if os.path.isfile(data_path):
                    import json as _json
                    with open(data_path, "r", encoding="utf-8") as f:
                        catalog = _json.load(f)
                ql = (query or "").lower()
                locl = (location or "").lower()
                chosen = None
                for m in catalog:
                    nm = str(m.get("name", "")).lower()
                    if nm and ((nm in ql) or (ql in nm) or (nm in locl) or (locl in nm)):
                        chosen = m
                        break
                if not chosen and catalog:
                    chosen = catalog[0]
                desc = (chosen or {}).get("description", "No description available.")
                facts = (chosen or {}).get("facts", [])
                extra = facts[0] if isinstance(facts, list) and facts else ""
                answer = (f"{(chosen or {}).get('name', 'This monument')}: {desc} " + (extra or "")).strip()
            except Exception:
                answer = "I'm here to help with monuments. Could you try asking about a specific landmark or provide a location?"

        payload = {
            "answer": answer,
            "confidence": 0.0,
            "related_monuments": [],
            "model": model_used or "fallback",
        }
        await sio.emit("assistant_response", payload, to=sid)
    except Exception as e:
        logging.error(f"Error in assistant_query: {e}", exc_info=True)
        try:
            data_path = os.path.join(os.path.dirname(__file__), "data", "monuments.json")
            catalog = []
            if os.path.isfile(data_path):
                import json as _json
                with open(data_path, "r", encoding="utf-8") as f:
                    catalog = _json.load(f)
            ql = (data.get("query") or "").lower() if isinstance(data, dict) else ""
            locl = (data.get("location") or "").lower() if isinstance(data, dict) else ""
            chosen = None
            for m in catalog:
                nm = str(m.get("name", "")).lower()
                if nm and ((nm in ql) or (ql in nm) or (nm in locl) or (locl in nm)):
                    chosen = m
                    break
            if not chosen and catalog:
                chosen = catalog[0]
            desc = (chosen or {}).get("description", "No description available.")
            facts = (chosen or {}).get("facts", [])
            extra = facts[0] if isinstance(facts, list) and facts else ""
            fallback_answer = (f"{(chosen or {}).get('name', 'This monument')}: {desc} " + (extra or "")).strip()
        except Exception:
            fallback_answer = "I'm here to help with monuments. Could you try asking about a specific landmark or provide a location?"
        await sio.emit("assistant_response", {"answer": fallback_answer, "confidence": 0.0, "related_monuments": []}, to=sid)

from services.vision_service import routes as vision_routes
from services.diary_service import routes as diary_routes

app.include_router(vision_routes.router)
app.include_router(diary_routes.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TRAVO API (Diary Mode)",
        "docs": "/docs",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
