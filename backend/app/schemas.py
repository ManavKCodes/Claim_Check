from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class ProductLookupRequest(BaseModel):
    barcode: str | None = Field(default=None, max_length=32)
    product_url: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def require_identifier(self) -> "ProductLookupRequest":
        if not self.barcode and not self.product_url:
            raise ValueError("barcode or product_url is required")
        return self


class ProductLookupResponse(BaseModel):
    barcode: str
    name: str | None
    brand: str | None
    categories: list[str]
    product_family: str | None
    ingredients_text: str | None
    nutriments: dict[str, object]
    images: list[dict[str, str]]
    source_name: str
    source_reference: str


class ClaimExtractionRequest(BaseModel):
    raw_text: str = Field(min_length=1, max_length=2000)
    source: str = Field(default="user_input", min_length=1, max_length=100)


class ClaimExtractionResponse(BaseModel):
    raw_claim: str
    normalized_claim: str | None
    claim_type: str | None
    extraction_method: str
    confidence: float | None
    source: str


class ComparatorProduct(BaseModel):
    product_id: str = Field(min_length=1, max_length=100)
    category: str | None = Field(default=None, max_length=200)
    product_family: str | None = Field(default=None, max_length=200)
    brand: str | None = Field(default=None, max_length=200)
    basis: str | None = Field(default=None, max_length=80)
    nutrient: str = Field(min_length=1, max_length=80)
    value: Decimal | None = None
    unit: str | None = Field(default=None, max_length=30)


class ComparatorResolutionRequest(BaseModel):
    subject: ComparatorProduct
    candidates: list[ComparatorProduct] = Field(default_factory=list, max_length=100)


class ComparatorResolutionResponse(BaseModel):
    status: str
    reference_product: ComparatorProduct | None
    candidate_count: int
    matching_factors: dict[str, str]
    notes: str


class EvidenceItemRequest(BaseModel):
    field_name: str = Field(min_length=1, max_length=120)
    source_type: str = Field(min_length=1, max_length=80)
    source_reference: str | None = Field(default=None, max_length=1000)
    image_reference: str | None = Field(default=None, max_length=1000)
    raw_value: str | None = Field(default=None, max_length=2000)
    normalized_value: str | None = Field(default=None, max_length=300)
    unit: str | None = Field(default=None, max_length=30)
    extraction_method: str | None = Field(default=None, max_length=80)
    confidence: float | None = Field(default=None, ge=0, le=1)


class EvidenceCompletenessRequest(BaseModel):
    required_fields: list[str] = Field(min_length=1, max_length=50)
    evidence: list[EvidenceItemRequest] = Field(default_factory=list, max_length=200)


class EvidenceCompletenessResponse(BaseModel):
    required_fields: list[str]
    present_fields: list[str]
    missing_fields: list[str]
    score: float


class ClaimClassificationRequest(BaseModel):
    raw_text: str = Field(min_length=1, max_length=2000)


class ClaimClassificationResponse(BaseModel):
    raw_claim: str
    claim_type: str | None
    display_name: str | None
    category: str | None
    nutrient: str | None
    requires_comparator: bool | None
    required_evidence: list[str]


class ProductAnalyzeRequest(BaseModel):
    product_name: str | None = Field(default=None, max_length=300)
    product_source_reference: str | None = Field(default=None, max_length=1000)
    claim_text: str = Field(min_length=1, max_length=2000)
    source: str = Field(default="user_input", min_length=1, max_length=100)


class ProductAnalyzeResponse(BaseModel):
    product_name: str | None
    product_source_reference: str | None
    claim: ClaimExtractionResponse
    status: str


class VerificationEvidenceRequest(EvidenceItemRequest):
    pass


class VerificationRequest(BaseModel):
    claim_type: str = Field(min_length=1, max_length=80)
    raw_claim: str = Field(min_length=1, max_length=2000)
    evidence: list[VerificationEvidenceRequest] = Field(default_factory=list, max_length=200)
    comparator_status: str | None = Field(default=None, max_length=40)
    comparator_details: dict[str, object] | None = None


class VerificationResponse(BaseModel):
    verification_id: str
    claim_type: str
    verdict: str
    rule_id: str
    rule_version: str | None
    calculation: dict[str, object] | None
    evidence_completeness: float
    missing_evidence: list[str]
    evidence: list[EvidenceItemRequest]
