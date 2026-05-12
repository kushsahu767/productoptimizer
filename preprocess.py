"""Text normalization and query understanding helpers."""

from __future__ import annotations

import re
from typing import Iterable


STOPWORDS = {
    "for",
    "with",
    "and",
    "the",
    "by",
    "men",
    "mens",
    "women",
    "womens",
    "edition",
    "smartphone",
    "shoe",
    "shoes",
    "running",
    "wireless",
    "noise",
    "canceling",
    "cancelling",
    "gps",
}

KNOWN_BRANDS = {
    "apple",
    "samsung",
    "nike",
    "adidas",
    "sony",
    "asus",
}

CATEGORY_HINTS = {
    "shoe",
    "shoes",
    "sneaker",
    "sneakers",
    "laptop",
    "headphone",
    "headphones",
    "smartwatch",
    "watch",
    "phone",
    "gaming",
}


def normalize_title(title: str) -> str:
    lowered = title.lower().strip()
    alphanumeric = re.sub(r"[^a-z0-9\s]", " ", lowered)
    collapsed = re.sub(r"\s+", " ", alphanumeric).strip()
    tokens = [token for token in collapsed.split() if token not in STOPWORDS]
    return " ".join(tokens)


def tokenize(text: str) -> list[str]:
    return normalize_title(text).split()


def extract_brand(text: str) -> str:
    tokens = tokenize(text)
    for token in tokens:
        if token in KNOWN_BRANDS:
            return token.title()
    return ""


def extract_attributes(text: str) -> dict[str, str | list[str]]:
    tokens = tokenize(text)
    brand = extract_brand(text)
    storage = next((token for token in tokens if re.fullmatch(r"\d+(gb|tb|mm)", token)), "")
    model_tokens = [token for token in tokens if token not in STOPWORDS and token != brand.lower()]
    important_keywords = [token for token in model_tokens if len(token) > 1][:6]

    return {
        "brand": brand,
        "model": " ".join(model_tokens[:4]).strip(),
        "storage": storage,
        "keywords": important_keywords,
    }


def detect_query_type(query: str) -> str:
    tokens = tokenize(query)
    if not tokens:
        return "general"

    has_numeric_detail = any(any(char.isdigit() for char in token) for token in tokens)
    has_category_hint = any(token in CATEGORY_HINTS for token in tokens)

    if has_numeric_detail or len(tokens) >= 3 and not has_category_hint:
        return "specific"
    if has_category_hint or len(tokens) <= 2:
        return "category"
    return "general"


def keyword_overlap(source: Iterable[str], target: Iterable[str]) -> float:
    source_set = set(source)
    target_set = set(target)
    if not source_set or not target_set:
        return 0.0
    return len(source_set & target_set) / len(source_set | target_set)
