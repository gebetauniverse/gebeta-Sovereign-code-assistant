Standardized error response schemas.
"""

from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    status: int
    detail: Optional[str] = None