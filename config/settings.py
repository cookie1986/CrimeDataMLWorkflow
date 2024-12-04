from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    MASTER_DATA_FILE: str = Field(..., description="Path to the master data file.")
    LOCAL_DATA_FILE_PATH: str = Field(..., description="Path to the sub-directory where the local version should be stored.")
    FILTER_COLUMNS: Optional[List[str]] = Field(None, description="Optional list of columns to be included when filtering the data.")

    class Config:
        env_file="config/.env"
        
    # preprocess the FILTER_COLUMNS value from a comma-separated string to a list.
    @field_validator("FILTER_COLUMNS", mode="before")
    def parse_filter_columns(value: Optional[str]) -> Optional[List[str]]:
        if value is None:
            return None
        # split FILTER_COLUMNS string by comma
        return [col.strip() for col in value.split(",")]

    def __init__(self, **data):
        super().__init__(**data)
        if isinstance(self.FILTER_COLUMNS, str):
            self.FILTER_COLUMNS = self.parse_filter_columns(self.FILTER_COLUMNS)


# instantiate settings
settings = Settings()