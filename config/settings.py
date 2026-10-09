import os


class Settings:

    APP_NAME: str = os.getenv("APP_NAME", "HSE Document Finder")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.2")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    def as_dict(self) -> dict:
        return {
            "APP_NAME": self.APP_NAME,
            "APP_VERSION": self.APP_VERSION,
            "LOG_LEVEL": self.LOG_LEVEL,
        }


settings = Settings()
