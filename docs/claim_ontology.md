# Claim Ontology

The ontology is configuration-driven and extensible. A claim record contains `claim_type`, `display_name`, `category`, `nutrient`, `requires_comparator`, `required_evidence`, and `allowed_extraction_sources`.

| Claim type | Display name | Category | Nutrient | Comparator | Required evidence |
| --- | --- | --- | --- | --- | --- |
| `HIGH_PROTEIN` | High Protein | absolute | protein | No | claim, subject protein, applicable rule |
| `LOW_FAT` | Low Fat | absolute | fat | No | claim, subject fat, applicable rule |
| `NO_ADDED_SUGAR` | No Added Sugar | ingredient-condition | sugar | No | claim, ingredient list, applicable rule |
| `COMPARATIVE_PROTEIN` | 30% More Protein | comparative | protein | Yes | claim, subject protein, reference product, reference protein, comparable basis, rule |
| `REDUCED_SODIUM` | Reduced Sodium | comparative | sodium | Yes | claim, subject sodium, reference product, reference sodium, comparable basis, rule |

Raw claim text is retained. Normalization may use deterministic patterns or an ML-assisted candidate generator, but the final normalized type must be validated against this ontology. Unknown or ambiguous text is not forced into a known type.

Thresholds and conditions are deliberately absent from this ontology; they belong to sourced, versioned rules.
