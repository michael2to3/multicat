from typing import Any, Optional
from pydantic import BaseModel, Field


class CeleryResponse(BaseModel):
    error: str = Field(default="", description="Error message, if any")
    warning: str = Field(default="", description="Warning message, if any")
    value: Optional[Any] = Field(
        default=None, description="The response value from the task, can be of any type"
    )
