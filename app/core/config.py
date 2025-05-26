from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str  
    DATABASE_URL_SYNC: str  
    SECRET_KEY: str  
    admin_email: str      
    admin_password: str   
    WHATSAPP_INSTANCE_ID: str
    WHATSAPP_TOKEN: str
    sentry_dsn: str | None = None
    class Config:
        env_file = ".env"

settings = Settings()
