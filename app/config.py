from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str
    STRIPE_API_KEY: str
    PAYFAST_MERCHANT_ID: str
    PAYFAST_MERCHANT_KEY: str
    PAYFAST_PASSPHRASE: str
    PAYFAST_SANDBOX: bool

    @property
    def PAYFAST_URL(self) -> str:
        return "https://sandbox.payfast.co.za" if self.PAYFAST_SANDBOX else "https://www.payfast.co.za"

    class Config:
        env_file = ".env"

settings = Settings() 