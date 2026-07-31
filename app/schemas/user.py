from pydantic import BaseModel


class LoginSchema(BaseModel):
    """Request body for login."""

    username: str
    password: str


class RegisterSchema(BaseModel):
    """Request body for register."""

    username: str
    password: str


class RefreshTokenSchema(BaseModel):
    """Request body for token refresh."""

    refresh_token: str
