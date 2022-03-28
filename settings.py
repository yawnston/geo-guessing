import os
from pathlib import Path
from pydantic import BaseSettings

_ROOT_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # Replace the API key in .env.local file by adding a line like this:
    # geo_google_api_key="API_KEY_GOES_HERE"
    # The .env.local file is automatically loaded into the settings,
    # and is ignored by git, so we use it to keep the API key.
    google_api_key: str = "PLACEHOLDER"

    maps_metadata_url = "https://maps.googleapis.com/maps/api/streetview/metadata?"
    maps_image_url = "https://maps.googleapis.com/maps/api/streetview?"

    api_bind_host: str = "localhost"
    api_bind_port: int = 8081

    class Config:
        env_prefix = "geo_"
        env_file = _ROOT_DIR / ".env.local"
        case_sensitive = False


# Global app settings instance
SETTINGS = Settings()
