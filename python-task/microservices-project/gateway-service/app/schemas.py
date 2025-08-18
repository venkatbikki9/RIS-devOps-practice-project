from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    service: str
    dependencies: Optional[dict] = None
    error: Optional[str] = None