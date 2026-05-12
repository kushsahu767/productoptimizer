"""Fuzzy matching engine."""

from __future__ import annotations

from rapidfuzz import fuzz

from preprocess import extract_attributes, normalize_title


def similarity(title1: str, title2: str) -> float:
    normalized_1 = normalize_title(title1)
    normalized_2 = normalize_title(title2)

    base_ratio = fuzz.token_sort_ratio(normalized_1, normalized_2)
    partial_ratio = fuzz.partial_ratio(normalized_1, normalized_2)

    attrs_1 = extract_attributes(title1)
    attrs_2 = extract_attributes(title2)

    brand_bonus = 7 if attrs_1["brand"] and attrs_1["brand"] == attrs_2["brand"] else -10
    storage_bonus = 5 if attrs_1["storage"] and attrs_1["storage"] == attrs_2["storage"] else 0

    keyword_overlap = len(set(attrs_1["keywords"]) & set(attrs_2["keywords"]))
    keyword_bonus = min(keyword_overlap * 2, 8)

    final_score = (base_ratio * 0.7) + (partial_ratio * 0.3) + brand_bonus + storage_bonus + keyword_bonus
    return round(max(0.0, min(final_score, 100.0)), 2)
