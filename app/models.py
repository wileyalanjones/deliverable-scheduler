from __future__ import annotations

from datetime import datetime, date
from enum import Enum as PyEnum
from sqlalchemy import (
    ForeignKey, 
    String, 
    Enum as SAEnum, 
    DateTime,
    Date, 
    Boolean, 
    Float,
    Text,
    func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class AuthProvider(str, PyEnum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    DEMO = "demo"


class Provider(str, PyEnum):
    GOOGLE = "google"
    OUTLOOK = "outlook"
    MOCK = "mock"


class FileType(str, PyEnum):
    PDF = "pdf"
    DOC = "docx"
    EML = "eml"


class FileStatus(str, PyEnum):
    UPLOADED = "uploaded"
    PARSED = "parsed"
    FAILED = "failed"


class ItemStatus(str, PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    auth_provider: Mapped[AuthProvider] = mapped_column(SAEnum(AuthProvider))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    connections: Mapped[list["CalendarConnection"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class CalendarConnection(Base):
    __tablename__ = "calendar_connections"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  
    provider: Mapped[Provider] = mapped_column(SAEnum(Provider))
    access_token: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    refresh_token: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean, 
        default=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    user: Mapped["User"] = relationship(back_populates="connections")


class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    filename: Mapped[str] = mapped_column(String(100))
    file_type: Mapped[FileType] = mapped_column(SAEnum(FileType))
    status: Mapped[FileStatus] = mapped_column(SAEnum(FileStatus))
    parsed_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    items: Mapped[list["ExtractedItem"]] = relationship(back_populates="document")
    

class ExtractedItem(Base):
    __tablename__ = "extracted_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    title: Mapped[str] = mapped_column(String(64))
    deliverable_date: Mapped[date] = mapped_column(Date)
    description:  Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    confidence: Mapped[float] = mapped_column(Float)
    source_quote: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    status: Mapped[ItemStatus] = mapped_column(SAEnum(ItemStatus))
    target_connection_id: Mapped[int | None] = mapped_column(
        ForeignKey("calendar_connections.id"),
        nullable=True
    )
    provider_event_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    document: Mapped["Document"] = relationship(back_populates="items")