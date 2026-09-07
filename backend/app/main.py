from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.claim_engine.extraction import extract_claim
from app.claim_engine.ontology.catalog import CLAIM_BY_TYPE
from app.comparator.resolver import ProductCandidate, resolve_comparator
from app.database import get_db
from app.evidence.trail import EvidenceItem, calculate_completeness
from app.evaluation.runner import run_evaluation
from app.product_sources.open_food_facts import (
    InvalidProductIdentifier,
    OpenFoodFactsClient,
    ProductNotFound,
    ProductSourceUnavailable,
)
from app.rule_engine.rules.catalog import RULE_CATALOG
from app.verification.service import verify_claim
from app.schemas import (
    ClaimExtractionRequest,
    ClaimExtractionResponse,
    ClaimClassificationRequest,
    ClaimClassificationResponse,
    ComparatorProduct,
    ComparatorResolutionRequest,
    ComparatorResolutionResponse,
    EvidenceCompletenessRequest,
    EvidenceCompletenessResponse,
    EvidenceItemRequest,
    ProductAnalyzeRequest,
    ProductAnalyzeResponse,
    ProductLookupRequest,
    ProductLookupResponse,
    VerificationRequest,
    VerificationResponse,
)
from app.settings import get_settings

settings = get_settings()
app = FastAPI(
    title="ClaimCheck API",
    version="0.1.0",
    description="Evidence-screening API for packaged food claims in India.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env}


@app.get("/health/database", tags=["system"])
def database_health() -> dict[str, str]:
    database_session = next(get_db())
    database_session.close()
    return {"status": "configured", "database": settings.database_url.split(":", 1)[0]}


@app.post("/api/product/lookup", response_model=ProductLookupResponse, tags=["products"])
def product_lookup(request: ProductLookupRequest) -> ProductLookupResponse:
    client = OpenFoodFactsClient(
        base_url=settings.openfoodfacts_base_url,
        user_agent=settings.openfoodfacts_user_agent,
        timeout_seconds=settings.openfoodfacts_timeout_seconds,
    )
    try:
        product = client.lookup(barcode=request.barcode, product_url=request.product_url)
    except InvalidProductIdentifier as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ProductNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ProductSourceUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ProductLookupResponse.model_validate(product.__dict__)


@app.post("/api/claim/extract", response_model=ClaimExtractionResponse, tags=["claims"])
def claim_extract(request: ClaimExtractionRequest) -> ClaimExtractionResponse:
    return ClaimExtractionResponse.model_validate(extract_claim(request.raw_text, request.source).__dict__)


@app.post("/api/claim/classify", response_model=ClaimClassificationResponse, tags=["claims"])
def claim_classify(request: ClaimClassificationRequest) -> ClaimClassificationResponse:
    extracted = extract_claim(request.raw_text)
    definition = CLAIM_BY_TYPE.get(extracted.claim_type or "")
    return ClaimClassificationResponse(
        raw_claim=extracted.raw_claim,
        claim_type=extracted.claim_type,
        display_name=definition.display_name if definition else None,
        category=definition.category if definition else None,
        nutrient=definition.nutrient if definition else None,
        requires_comparator=definition.requires_comparator if definition else None,
        required_evidence=list(definition.required_evidence) if definition else [],
    )


@app.post("/api/product/analyze", response_model=ProductAnalyzeResponse, tags=["products"])
def product_analyze(request: ProductAnalyzeRequest) -> ProductAnalyzeResponse:
    claim = ClaimExtractionResponse.model_validate(extract_claim(request.claim_text, request.source).__dict__)
    return ProductAnalyzeResponse(
        product_name=request.product_name,
        product_source_reference=request.product_source_reference,
        claim=claim,
        status="claim_candidate_extracted",
    )


@app.post("/api/comparator/resolve", response_model=ComparatorResolutionResponse, tags=["comparators"])
def comparator_resolve(request: ComparatorResolutionRequest) -> ComparatorResolutionResponse:
    subject = ProductCandidate(**request.subject.model_dump())
    candidates = [ProductCandidate(**candidate.model_dump()) for candidate in request.candidates]
    resolution = resolve_comparator(subject, candidates)
    return ComparatorResolutionResponse(
        status=resolution.status,
        reference_product=(
            ComparatorProduct.model_validate(resolution.reference_product.__dict__)
            if resolution.reference_product
            else None
        ),
        candidate_count=resolution.candidate_count,
        matching_factors=resolution.matching_factors,
        notes=resolution.notes,
    )


@app.post("/api/evidence/completeness", response_model=EvidenceCompletenessResponse, tags=["evidence"])
def evidence_completeness(request: EvidenceCompletenessRequest) -> EvidenceCompletenessResponse:
    evidence = [EvidenceItem.create(**item.model_dump()) for item in request.evidence]
    completeness = calculate_completeness(request.required_fields, evidence)
    return EvidenceCompletenessResponse(
        required_fields=list(completeness.required_fields),
        present_fields=list(completeness.present_fields),
        missing_fields=list(completeness.missing_fields),
        score=completeness.score,
    )


@app.post("/api/verify", response_model=VerificationResponse, tags=["verification"])
def verify(request: VerificationRequest) -> VerificationResponse:
    evidence = [EvidenceItem.create(**item.model_dump()) for item in request.evidence]
    result = verify_claim(
        claim_type=request.claim_type,
        raw_claim=request.raw_claim,
        evidence=evidence,
        comparator_status=request.comparator_status,
        comparator_details=request.comparator_details,
    )
    return VerificationResponse(
        verification_id=result.verification_id,
        claim_type=result.claim_type,
        verdict=result.evaluation.verdict,
        rule_id=result.evaluation.rule_id,
        rule_version=result.rule.regulation_version if result.rule else None,
        calculation=result.evaluation.calculation,
        evidence_completeness=result.trail.completeness.score,
        missing_evidence=list(result.evaluation.missing_evidence or result.trail.completeness.missing_fields),
        evidence=[EvidenceItemRequest.model_validate(item.__dict__) for item in result.trail.evidence],
    )


@app.get("/api/rules", tags=["rules"])
def rules_catalog() -> list[dict[str, object]]:
    return [
        {
            "rule_id": rule.rule_id,
            "claim_type": rule.claim_type,
            "regulation_name": rule.regulation_name,
            "regulation_version": rule.regulation_version,
            "effective_date": rule.effective_date,
            "nutrient": rule.nutrient,
            "threshold": str(rule.threshold) if rule.threshold is not None else None,
            "threshold_type": rule.threshold_type,
            "unit": rule.unit,
            "applicable_conditions": rule.applicable_conditions,
            "calculation_method": rule.calculation_method,
            "evidence_requirements": list(rule.evidence_requirements),
            "source_reference": rule.source_reference,
            "notes": rule.notes,
            "status": rule.status,
        }
        for rule in RULE_CATALOG
    ]


@app.post("/api/evaluation/run", tags=["evaluation"])
def evaluation_run() -> dict[str, object]:
    benchmark_path = Path(settings.benchmark_path)
    return run_evaluation(benchmark_path)
