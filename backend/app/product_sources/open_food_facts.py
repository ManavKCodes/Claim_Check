import re
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx


class ProductSourceError(Exception):
    """Base error for a product source request."""


class InvalidProductIdentifier(ProductSourceError):
    """The supplied barcode or product URL is not supported."""


class ProductNotFound(ProductSourceError):
    """The product source does not contain the requested product."""


class ProductSourceUnavailable(ProductSourceError):
    """The product source could not be reached or returned invalid data."""


@dataclass(frozen=True)
class ProductLookup:
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


class OpenFoodFactsClient:
    """Client for the Open Food Facts product API, kept behind a source boundary."""

    source_name = "Open Food Facts"
    barcode_pattern = re.compile(r"^\d{8,14}$")

    def __init__(self, base_url: str, user_agent: str, timeout_seconds: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.user_agent = user_agent
        self.timeout_seconds = timeout_seconds

    def lookup(self, barcode: str | None = None, product_url: str | None = None) -> ProductLookup:
        normalized_barcode = self._resolve_barcode(barcode, product_url)
        endpoint = f"{self.base_url}/api/v2/product/{normalized_barcode}.json"
        try:
            response = httpx.get(
                endpoint,
                headers={"User-Agent": self.user_agent, "Accept": "application/json"},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ProductSourceUnavailable("Open Food Facts is unavailable") from exc

        if payload.get("status") != 1 or not isinstance(payload.get("product"), dict):
            raise ProductNotFound("Product was not found in Open Food Facts")
        return self._normalize_product(normalized_barcode, payload["product"])

    def _resolve_barcode(self, barcode: str | None, product_url: str | None) -> str:
        if barcode:
            normalized = barcode.strip()
            if self.barcode_pattern.fullmatch(normalized):
                return normalized
            raise InvalidProductIdentifier("Barcode must contain 8 to 14 digits")
        if product_url:
            parsed = urlparse(product_url.strip())
            path_parts = [part for part in parsed.path.split("/") if part]
            candidate = path_parts[-1] if path_parts else ""
            if parsed.scheme in {"http", "https"} and self.barcode_pattern.fullmatch(candidate):
                return candidate
        raise InvalidProductIdentifier("Provide a valid barcode or product URL")

    def _normalize_product(self, barcode: str, product: dict[str, object]) -> ProductLookup:
        categories = self._split_labels(product.get("categories_tags"))
        images: list[dict[str, str]] = []
        for image_key in ("front_url", "ingredients_url", "nutrition_url"):
            image_url = product.get(image_key)
            if isinstance(image_url, str) and image_url:
                images.append({"image_type": image_key.removesuffix("_url"), "image_url": image_url})
        return ProductLookup(
            barcode=barcode,
            name=self._string_value(product.get("product_name")),
            brand=self._string_value(product.get("brands")),
            categories=categories,
            product_family=self._string_value(product.get("generic_name")),
            ingredients_text=self._string_value(product.get("ingredients_text")),
            nutriments=product.get("nutriments") if isinstance(product.get("nutriments"), dict) else {},
            images=images,
            source_name=self.source_name,
            source_reference=f"{self.base_url}/product/{barcode}",
        )

    @staticmethod
    def _string_value(value: object) -> str | None:
        return value.strip() if isinstance(value, str) and value.strip() else None

    @staticmethod
    def _split_labels(value: object) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, str)]
