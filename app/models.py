import reflex as rx

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from typing import ClassVar

JSONValue = (
    str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
)

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    MetaData,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class UserAccount(Base):
    __tablename__ = "cvpro_users"
    __table_args__ = (
        CheckConstraint("length(btrim(sub)) > 0", name="sub_not_empty"),
        CheckConstraint("role IN ('admin', 'member')", name="valid_role"),
    )

    sub: Mapped[str] = mapped_column(
        String(255), primary_key=True, default="", server_default=""
    )
    email: Mapped[str] = mapped_column(
        String(320), default="", server_default=""
    )
    name: Mapped[str] = mapped_column(
        String(255), default="", server_default=""
    )
    role: Mapped[str] = mapped_column(
        String(16), default="member", server_default="member"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CVTemplate(Base):
    __tablename__ = "cvpro_templates"
    CATALOG: ClassVar[tuple[tuple[str, str, int], ...]] = (
        ("moderne", "Moderne", 0),
        ("classique", "Classique", 1),
        ("elegant", "Élégant", 2),
        ("minimaliste", "Minimaliste", 3),
        ("creatif", "Créatif", 4),
    )
    __table_args__ = (
        CheckConstraint(
            "code IN ('moderne', 'classique', 'elegant', 'minimaliste', 'creatif')",
            name="five_template_codes",
        ),
        CheckConstraint(
            "display_order BETWEEN 0 AND 4", name="valid_display_order"
        ),
    )

    code: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        default="moderne",
        server_default="moderne",
    )
    name: Mapped[str] = mapped_column(
        String(100), default="", server_default=""
    )
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )
    display_order: Mapped[int] = mapped_column(
        SmallInteger, default=0, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CurriculumVitae(Base):
    __tablename__ = "cvpro_cvs"
    __table_args__ = (
        UniqueConstraint("id", "owner_sub", name="uq_cvpro_cvs_id_owner"),
        CheckConstraint("length(btrim(owner_sub)) > 0", name="owner_not_empty"),
        CheckConstraint("length(btrim(title)) > 0", name="title_not_empty"),
        CheckConstraint("schema_version >= 1", name="positive_schema_version"),
        CheckConstraint(
            "jsonb_typeof(information) = 'object'", name="information_object"
        ),
        CheckConstraint(
            "jsonb_typeof(sections) = 'array'", name="sections_array"
        ),
        Index("ix_cvpro_cvs_owner_updated", "owner_sub", "updated_at"),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    owner_sub: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("cvpro_users.sub", ondelete="RESTRICT"),
        default="",
        server_default="",
    )
    title: Mapped[str] = mapped_column(
        String(255), default="Mon CV", server_default="Mon CV"
    )
    template_code: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("cvpro_templates.code", ondelete="RESTRICT"),
        default="moderne",
        server_default="moderne",
    )
    schema_version: Mapped[int] = mapped_column(
        Integer, default=1, server_default="1"
    )
    information: Mapped[dict[str, JSONValue]] = mapped_column(
        JSONB, default=dict, server_default=text("'{}'::jsonb")
    )
    sections: Mapped[list[dict[str, JSONValue]]] = mapped_column(
        JSONB, default=list, server_default=text("'[]'::jsonb")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class PremiumPrice(Base):
    __tablename__ = "cvpro_premium_price"
    __table_args__ = (
        CheckConstraint("id = 1", name="singleton"),
        CheckConstraint("amount_dzd >= 0", name="nonnegative_amount"),
        CheckConstraint("currency = 'DZD'", name="dzd_only"),
    )

    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        default=1,
        server_default="1",
        autoincrement=False,
    )
    amount_dzd: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0.00"), server_default="0.00"
    )
    currency: Mapped[str] = mapped_column(
        String(3), default="DZD", server_default="DZD"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class DemoPurchase(Base):
    __tablename__ = "cvpro_demo_purchases"
    __table_args__ = (
        ForeignKeyConstraint(
            ["cv_id", "owner_sub"],
            ["cvpro_cvs.id", "cvpro_cvs.owner_sub"],
            ondelete="RESTRICT",
            name="fk_cvpro_purchase_owned_cv",
        ),
        CheckConstraint("length(btrim(owner_sub)) > 0", name="owner_not_empty"),
        CheckConstraint("price_dzd >= 0", name="nonnegative_price"),
        CheckConstraint("currency = 'DZD'", name="dzd_only"),
        CheckConstraint(
            "status IN ('pending', 'confirmed', 'cancelled')",
            name="valid_status",
        ),
        CheckConstraint("is_demo = true", name="demo_only"),
        Index(
            "ix_cvpro_demo_purchases_owner_created", "owner_sub", "created_at"
        ),
        Index("ix_cvpro_demo_purchases_cv_owner", "cv_id", "owner_sub"),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    owner_sub: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("cvpro_users.sub", ondelete="RESTRICT"),
        default="",
        server_default="",
    )
    cv_id: Mapped[UUID] = mapped_column(
        default=lambda: UUID(int=0),
        server_default=text("'00000000-0000-0000-0000-000000000000'::uuid"),
    )
    price_dzd: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0.00"), server_default="0.00"
    )
    currency: Mapped[str] = mapped_column(
        String(3), default="DZD", server_default="DZD"
    )
    status: Mapped[str] = mapped_column(
        String(16), default="pending", server_default="pending"
    )
    is_demo: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class AdminBootstrapLock(Base):
    __tablename__ = "cvpro_admin_bootstrap"
    __table_args__ = (
        CheckConstraint("id = 1", name="singleton"),
        CheckConstraint(
            "length(btrim(admin_sub)) > 0", name="admin_sub_not_empty"
        ),
    )

    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        default=1,
        server_default="1",
        autoincrement=False,
    )
    admin_sub: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("cvpro_users.sub", ondelete="RESTRICT"),
        unique=True,
        default="",
        server_default="",
    )
    claimed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
