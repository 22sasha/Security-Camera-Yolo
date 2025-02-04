from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class CameraConfig(Base): 
    __tablename__ = 'camera_configs' 

    name: Mapped[str] = mapped_column(String(128), unique=True)
    url: Mapped[str] = mapped_column(String(256))
