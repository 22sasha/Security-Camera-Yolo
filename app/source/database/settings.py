from pydantic import BaseModel
import os


class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: str
    db_name: str


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings(
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        db_name=os.environ.get("DB_NAME")
    )
