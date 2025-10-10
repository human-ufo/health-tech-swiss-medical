"""Configuration management for the application."""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_account_id: str = "862172028272"

    # AWS Bedrock
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    bedrock_region: str = "us-east-1"

    # DynamoDB Tables
    dynamodb_patients_table: str = "health-tech-patients"
    dynamodb_consultations_table: str = "health-tech-consultations"
    dynamodb_triage_table: str = "health-tech-triage"

    # LangSmith
    langchain_tracing_v2: bool = False
    langchain_endpoint: str = "https://api.smith.langchain.com"
    langchain_api_key: Optional[str] = None
    langchain_project: str = "swiss-medical-triage"

    # Application Settings
    app_name: str = "Swiss Medical Triage System"
    app_version: str = "1.0.0"
    environment: str = "development"
    log_level: str = "INFO"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Streamlit Settings
    streamlit_server_port: int = 8501
    streamlit_server_address: str = "0.0.0.0"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
