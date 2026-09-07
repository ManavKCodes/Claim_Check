# Phase 4: Open Food Facts Integration

Open Food Facts is used only as a product-data source. It is not the regulatory authority and does not determine ClaimCheck verdicts. FSSAI rule data remains a separate versioned concern.

## Adapter behavior

`OpenFoodFactsClient` calls the documented product API endpoint and normalizes product name, brand, categories, product family, ingredients text, nutriments, and packaging image URLs into a stable internal shape. The source URL and source name are retained for evidence provenance.

The adapter accepts an 8-14 digit barcode or an HTTPS product URL whose final path segment is an 8-14 digit barcode. It rejects malformed identifiers, treats missing products as not found, and maps network/HTTP/JSON failures to an unavailable-source error. It does not scrape pages or infer missing nutrition values.

The configured User-Agent and timeout are supplied through environment variables. Production deployment must set a contact-bearing User-Agent and respect Open Food Facts attribution, API usage, and rate-limit requirements.

## Boundary

This phase retrieves and normalizes product data only. It does not extract claims, select FSSAI rules, resolve comparators, or produce a verification verdict.
