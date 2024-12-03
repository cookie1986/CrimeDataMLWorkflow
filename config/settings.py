from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MASTER_DATA_FILE: str = Field(..., description="Path to the master data file.")
    LOCAL_DATA_FILE_PATH: str = Field(..., description="Path to the sub-directory where the local version should be stored.")

    class Config:
        env_file="config/.env"

# instantiate settings
settings = Settings()