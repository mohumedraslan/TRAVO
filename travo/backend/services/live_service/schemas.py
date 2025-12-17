from pydantic import BaseModel
from typing import Optional

class PulseRequest(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None

class PulseResponse(BaseModel):
    tip: str
    context: str
    status: str = "success"
