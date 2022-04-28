from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_base_uri: str
    position_uri: str
    client_id: str
    client_secret: str
    redirect_uri: str = "localhost"
    device_id: str = "DroneTag"
    access_token: Optional[str]

    class Config:
        env_file = ".env"


settings = Settings()
