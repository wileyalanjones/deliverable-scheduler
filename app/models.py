from datetime import datetime
from sqlalchemy import String, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column 

from database import Base


class AuthProvider(Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    DEMO = "demo"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    auth_provider: Mapped[str] = mapped_column(AuthProvider)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now())



    

