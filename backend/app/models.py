from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    barcode: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(300))
    brand: Mapped[str | None] = mapped_column(String(200), index=True)
    category: Mapped[str | None] = mapped_column(String(200), index=True)
    product_family: Mapped[str | None] = mapped_column(String(200), index=True)
    source_name: Mapped[str] = mapped_column(String(80), default="Open Food Facts")
    source_reference: Mapped[str | None] = mapped_column(String(500))
    source_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    images: Mapped[list["ProductImage"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    nutrition_data: Mapped[list["NutritionData"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    ingredients: Mapped[list["Ingredient"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    claims: Mapped[list["Claim"]] = relationship(back_populates="product", cascade="all, delete-orphan")


class ProductImage(TimestampMixin, Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    image_url: Mapped[str] = mapped_column(String(1000))
    image_type: Mapped[str | None] = mapped_column(String(80))
    region_reference: Mapped[str | None] = mapped_column(String(500))
    source_reference: Mapped[str | None] = mapped_column(String(500))

    product: Mapped[Product] = relationship(back_populates="images")


class NutritionData(TimestampMixin, Base):
    __tablename__ = "nutrition_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    nutrient: Mapped[str] = mapped_column(String(80), index=True)
    value: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    unit: Mapped[str | None] = mapped_column(String(30))
    basis: Mapped[str | None] = mapped_column(String(80))
    raw_value: Mapped[str | None] = mapped_column(String(200))
    source_reference: Mapped[str | None] = mapped_column(String(500))
    extraction_method: Mapped[str | None] = mapped_column(String(80))
    is_user_corrected: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped[Product] = relationship(back_populates="nutrition_data")


class Ingredient(TimestampMixin, Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    ingredient_text: Mapped[str] = mapped_column(Text)
    sequence: Mapped[int | None] = mapped_column(Integer)
    source_reference: Mapped[str | None] = mapped_column(String(500))
    extraction_method: Mapped[str | None] = mapped_column(String(80))
    is_user_corrected: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped[Product] = relationship(back_populates="ingredients")


class Claim(TimestampMixin, Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    raw_claim: Mapped[str] = mapped_column(Text)
    normalized_claim: Mapped[str | None] = mapped_column(String(100), index=True)
    claim_type: Mapped[str | None] = mapped_column(String(80), index=True)
    extraction_method: Mapped[str | None] = mapped_column(String(80))
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))
    source_reference: Mapped[str | None] = mapped_column(String(500))
    is_user_corrected: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped[Product] = relationship(back_populates="claims")


class Rule(TimestampMixin, Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    claim_type: Mapped[str] = mapped_column(String(80), index=True)
    regulation_name: Mapped[str] = mapped_column(String(300))
    regulation_version: Mapped[str] = mapped_column(String(100))
    effective_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    nutrient: Mapped[str | None] = mapped_column(String(80))
    threshold: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    threshold_type: Mapped[str | None] = mapped_column(String(80))
    unit: Mapped[str | None] = mapped_column(String(30))
    applicable_conditions: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    calculation_method: Mapped[str | None] = mapped_column(String(200))
    evidence_requirements: Mapped[list[str] | None] = mapped_column(JSON)
    source_reference: Mapped[str] = mapped_column(String(1000))
    notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="PENDING_SOURCE_VERIFICATION")


class Comparator(TimestampMixin, Base):
    __tablename__ = "comparators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    reference_product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), index=True)
    status: Mapped[str] = mapped_column(String(40))
    basis: Mapped[str | None] = mapped_column(String(80))
    candidate_count: Mapped[int] = mapped_column(Integer, default=0)
    matching_factors: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    resolution_notes: Mapped[str | None] = mapped_column(Text)


class Evidence(TimestampMixin, Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    verification_id: Mapped[int] = mapped_column(ForeignKey("verifications.id", ondelete="CASCADE"), index=True)
    source_type: Mapped[str] = mapped_column(String(80))
    source_reference: Mapped[str | None] = mapped_column(String(1000))
    image_reference: Mapped[str | None] = mapped_column(String(1000))
    field_name: Mapped[str] = mapped_column(String(120), index=True)
    raw_value: Mapped[str | None] = mapped_column(Text)
    normalized_value: Mapped[str | None] = mapped_column(String(300))
    unit: Mapped[str | None] = mapped_column(String(30))
    extraction_method: Mapped[str | None] = mapped_column(String(80))
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))

    verification: Mapped["Verification"] = relationship(back_populates="evidence")


class Verification(TimestampMixin, Base):
    __tablename__ = "verifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    claim_id: Mapped[int] = mapped_column(ForeignKey("claims.id"), index=True)
    rule_id: Mapped[int | None] = mapped_column(ForeignKey("rules.id"), index=True)
    comparator_id: Mapped[int | None] = mapped_column(ForeignKey("comparators.id"), index=True)
    calculation: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    verdict: Mapped[str] = mapped_column(String(40), index=True)
    evidence_completeness: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))
    missing_evidence: Mapped[list[str] | None] = mapped_column(JSON)

    evidence: Mapped[list[Evidence]] = relationship(back_populates="verification", cascade="all, delete-orphan")


class BenchmarkRecord(TimestampMixin, Base):
    __tablename__ = "benchmark_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), index=True)
    split: Mapped[str] = mapped_column(String(20), index=True)
    expected_verdict: Mapped[str] = mapped_column(String(40))
    claim_type: Mapped[str] = mapped_column(String(80))
    annotation_status: Mapped[str] = mapped_column(String(40), default="DRAFT")
    annotation_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    evidence_notes: Mapped[str | None] = mapped_column(Text)
    annotation_notes: Mapped[str | None] = mapped_column(Text)


class EvaluationResult(TimestampMixin, Base):
    __tablename__ = "evaluation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    benchmark_version: Mapped[str] = mapped_column(String(100))
    split_strategy: Mapped[str] = mapped_column(String(100))
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON)
    sample_count: Mapped[int] = mapped_column(Integer)
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


Index("ix_nutrition_product_nutrient_basis", NutritionData.product_id, NutritionData.nutrient, NutritionData.basis)
Index("ix_verification_product_claim", Verification.product_id, Verification.claim_id)
