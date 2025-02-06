from database.database import Base as DBBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DBBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
