from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class IPCamera(Base): 
    __tablename__ = 'ip_camera' 

    ip: Mapped[str] = mapped_column(String)
