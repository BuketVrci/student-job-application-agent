import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class TargetRoleType(str, enum.Enum):
    WERKSTUDENT = "werkstudent"
    PRAKTIKUM = "praktikum"
    EITHER = "either"


class LanguagePreference(str, enum.Enum):
    DE = "de"
    EN = "en"
    BOTH = "both"


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    field_of_study: Mapped[str | None] = mapped_column(String(255))
    target_role_type: Mapped[TargetRoleType] = mapped_column(
        String(20), default=TargetRoleType.EITHER
    )
    preferred_cities: Mapped[list[str]] = mapped_column(JSON, default=list)
    remote_ok: Mapped[bool] = mapped_column(Boolean, default=True)
    language_preference: Mapped[LanguagePreference] = mapped_column(
        String(10), default=LanguagePreference.BOTH
    )
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    base_cv_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="profile")
