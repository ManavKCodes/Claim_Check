import httpx
import pytest

from app.product_sources.open_food_facts import (
    InvalidProductIdentifier,
    OpenFoodFactsClient,
    ProductNotFound,
)


def test_lookup_normalizes_product_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(*args: object, **kwargs: object) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "status": 1,
                "product": {
                    "product_name": "Example Food",
                    "brands": "Example Brand",
                    "categories_tags": ["en:snacks"],
                    "generic_name": "Example family",
                    "ingredients_text": "Ingredient list",
                    "nutriments": {"proteins_100g": 12.0},
                    "front_url": "https://images.example/front.jpg",
                },
            },
            request=httpx.Request("GET", str(args[0])),
        )

    monkeypatch.setattr(httpx, "get", fake_get)
    result = OpenFoodFactsClient("https://world.openfoodfacts.org", "ClaimCheck/test").lookup(
        barcode="12345678"
    )

    assert result.name == "Example Food"
    assert result.categories == ["en:snacks"]
    assert result.nutriments["proteins_100g"] == 12.0
    assert result.source_name == "Open Food Facts"


def test_lookup_rejects_invalid_identifier() -> None:
    client = OpenFoodFactsClient("https://world.openfoodfacts.org", "ClaimCheck/test")

    with pytest.raises(InvalidProductIdentifier):
        client.lookup(barcode="not-a-barcode")


def test_lookup_extracts_barcode_from_product_url(monkeypatch: pytest.MonkeyPatch) -> None:
    requested_urls: list[str] = []

    def fake_get(url: str, **kwargs: object) -> httpx.Response:
        requested_urls.append(url)
        return httpx.Response(200, json={"status": 0, "product": {}}, request=httpx.Request("GET", url))

    monkeypatch.setattr(httpx, "get", fake_get)
    client = OpenFoodFactsClient("https://world.openfoodfacts.org", "ClaimCheck/test")

    with pytest.raises(ProductNotFound):
        client.lookup(product_url="https://world.openfoodfacts.org/product/12345678")

    assert requested_urls == ["https://world.openfoodfacts.org/api/v2/product/12345678.json"]
