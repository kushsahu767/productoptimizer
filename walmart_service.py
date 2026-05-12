"""Walmart product service with live/fallback modes."""

from __future__ import annotations

import os
from typing import Any

import requests

from data import SAMPLE_PRODUCTS
from preprocess import extract_brand, normalize_title


class WalmartService:
    def __init__(self) -> None:
        self.api_key = os.getenv("WALMART_API_KEY", "")
        self.api_url = os.getenv("WALMART_API_URL", "")

    def search_products(self, query: str) -> list[dict[str, Any]]:
        live_results = self._fetch_live(query)
        if live_results:
            return live_results
        return self._search_sample(query)

    def _fetch_live(self, query: str) -> list[dict[str, Any]]:
        if not self.api_key or not self.api_url:
            return []

        try:
            response = requests.get(
                self.api_url,
                params={"query": query, "apiKey": self.api_key},
                timeout=8,
            )
            response.raise_for_status()
            payload = response.json()
            items = payload.get("items", []) or payload.get("products", [])
            normalized_items = []
            for item in items:
                normalized_items.append(
                    {
                        "title": item.get("title", item.get("name", "")),
                        "price": float(item.get("price", item.get("salePrice", 0)) or 0),
                        "platform": "Walmart",
                        "rating": float(item.get("rating", item.get("customerRating", 0)) or 0),
                        "image": item.get("image", item.get("thumbnailImage", "")),
                        "link": item.get("link", item.get("productUrl", "")),
                        "brand": item.get("brand") or extract_brand(item.get("title", item.get("name", ""))),
                    }
                )
            return normalized_items
        except (requests.RequestException, ValueError, TypeError):
            return []

    def _search_sample(self, query: str) -> list[dict[str, Any]]:
        normalized_query = normalize_title(query)
        query_tokens = set(normalized_query.split())
        results = []

        for product in SAMPLE_PRODUCTS["walmart"]:
            title_tokens = set(normalize_title(product["title"]).split())
            if query_tokens <= title_tokens or query_tokens & title_tokens:
                results.append(product)

        return results[:10]
