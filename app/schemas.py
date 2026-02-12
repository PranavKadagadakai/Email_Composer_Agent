from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    to_email: EmailStr
    task: str = Field(..., min_length=5)
    tone: str | None = "professional"
    constraints: str | None = None
