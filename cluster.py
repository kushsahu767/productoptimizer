"""Greedy clustering and deal intelligence."""

from __future__ import annotations

from statistics import mean

from matcher import similarity
from preprocess import extract_attributes, normalize_title


def choose_representative(items: list[dict]) -> dict:
    scored = []
    for item in items:
        title_length = len(normalize_title(item["title"]))
        score = (item.get("rating", 0) * 10) + title_length - (item.get("price", 0) / 100)
        scored.append((score, item))
    scored.sort(key=lambda entry: entry[0], reverse=True)
    return scored[0][1]


def same_brand(item_a: dict, item_b: dict) -> bool:
    brand_a = (item_a.get("brand") or extract_attributes(item_a["title"])["brand"]).lower()
    brand_b = (item_b.get("brand") or extract_attributes(item_b["title"])["brand"]).lower()
    return bool(brand_a and brand_b and brand_a == brand_b)


def cluster_products(products: list[dict], threshold: float = 75.0) -> list[dict]:
    clusters: list[dict] = []

    for product in products:
        placed = False

        for cluster in clusters:
            representative = cluster["representative"]
            score = similarity(product["title"], representative["title"])

            if score >= threshold and same_brand(product, representative):
                cluster["items"].append({**product, "match_score": score})
                cluster["representative"] = choose_representative(cluster["items"])
                placed = True
                break

        if not placed:
            clusters.append(
                {
                    "representative": product,
                    "items": [{**product, "match_score": 100.0}],
                }
            )

    return [summarize_cluster(cluster["items"]) for cluster in clusters]


def summarize_cluster(items: list[dict]) -> dict:
    representative = choose_representative(items)
    sorted_items = sorted(items, key=lambda item: (item["price"], -item.get("rating", 0)))
    best_item = sorted_items[0]

    price_values = [item["price"] for item in items]
    avg_price = mean(price_values)
    lowest_price = min(price_values)
    highest_price = max(price_values)
    price_gap = highest_price - lowest_price

    best_value_item = max(
        items,
        key=lambda item: ((item.get("rating", 0) * 18) - item["price"] / 20),
    )

    return {
        "product_name": representative["title"],
        "normalized_name": normalize_title(representative["title"]),
        "brand": representative.get("brand") or extract_attributes(representative["title"])["brand"],
        "items": sorted_items,
        "best_platform": best_item["platform"],
        "best_price": best_item["price"],
        "best_rating": best_item.get("rating", 0),
        "best_value_platform": best_value_item["platform"],
        "best_value_price": best_value_item["price"],
        "avg_price": round(avg_price, 2),
        "price_gap": round(price_gap, 2),
        "cluster_size": len(items),
    }
