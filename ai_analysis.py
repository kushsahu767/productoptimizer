"""Gemini-backed market analysis with safe fallback summaries."""

from __future__ import annotations

import json
import os
from typing import Any

import requests


class GeminiAnalyzer:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-1.5-flash:generateContent"
        )

    def analyze_market(self, query: str, clusters: list[dict[str, Any]], query_type: str) -> dict[str, Any]:
        if self.api_key:
            live_response = self._call_gemini(query, clusters, query_type)
            if live_response:
                return live_response

        return self._fallback_analysis(query, clusters, query_type)

    def _call_gemini(
        self,
        query: str,
        clusters: list[dict[str, Any]],
        query_type: str,
    ) -> dict[str, Any] | None:
        compact_clusters = [
            {
                "product_name": cluster["product_name"],
                "best_platform": cluster["best_platform"],
                "best_price": cluster["best_price"],
                "price_gap": cluster["price_gap"],
                "ratings": [item.get("rating", 0) for item in cluster["items"]],
                "platforms": [item["platform"] for item in cluster["items"]],
            }
            for cluster in clusters[:6]
        ]

        prompt = f"""
You are a sharp ecommerce pricing analyst for a SaaS product called Product Price Optimiser.
Analyze the market for the search query "{query}".
Query type: {query_type}
Cluster data:
{json.dumps(compact_clusters, indent=2)}

Return only JSON with this exact shape:
{{
  "summary": "short executive summary",
  "recommendation": "buy now or wait",
  "market_trend": "trend insight",
  "highlights": ["bullet", "bullet", "bullet"],
  "cluster_summaries": {{
    "product_name": "cluster level insight"
  }}
}}
""".strip()

        try:
            response = requests.post(
                f"{self.endpoint}?key={self.api_key}",
                json={
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt},
                            ]
                        }
                    ]
                },
                timeout=12,
            )
            response.raise_for_status()
            payload = response.json()
            text = (
                payload.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            parsed = json.loads(cleaned)
            return {
                "summary": parsed.get("summary", ""),
                "recommendation": parsed.get("recommendation", ""),
                "market_trend": parsed.get("market_trend", ""),
                "highlights": parsed.get("highlights", []),
                "cluster_summaries": parsed.get("cluster_summaries", {}),
                "source": "gemini",
            }
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError):
            return None

    def _fallback_analysis(self, query: str, clusters: list[dict[str, Any]], query_type: str) -> dict[str, Any]:
        if not clusters:
            return {
                "summary": f'No matched listings were found for "{query}". Try a broader product or category search.',
                "recommendation": "search broader terms",
                "market_trend": "insufficient market data",
                "highlights": [
                    "No cross-platform matches were available.",
                    "Try a broader category or include fewer model-specific details.",
                    "API fallback data is ready once matching listings appear.",
                ],
                "cluster_summaries": {},
                "source": "fallback",
            }

        cheapest = min(clusters, key=lambda cluster: cluster["best_price"])
        largest_gap = max(clusters, key=lambda cluster: cluster["price_gap"])
        amazon_wins = sum(1 for cluster in clusters if cluster["best_platform"] == "Amazon")
        walmart_wins = sum(1 for cluster in clusters if cluster["best_platform"] == "Walmart")

        trend = "competitive pricing with narrow gaps"
        recommendation = "buy now"
        if largest_gap["price_gap"] >= 40:
            trend = "active discount spread across platforms"
        if query_type == "category":
            recommendation = "compare top clusters now and shortlist the lowest-gap listings"
        elif cheapest["best_price"] > sum(cluster["best_price"] for cluster in clusters) / len(clusters):
            recommendation = "wait for a better entry point"

        highlights = [
            f'{cheapest["best_platform"]} currently leads the "{cheapest["product_name"]}" cluster at ${cheapest["best_price"]:.0f}.',
            f'Largest spread is ${largest_gap["price_gap"]:.0f} on "{largest_gap["product_name"]}", signaling negotiation room.',
            f"Platform leadership: Amazon {amazon_wins} clusters, Walmart {walmart_wins} clusters.",
        ]

        cluster_summaries = {}
        for cluster in clusters:
            cluster_summaries[cluster["product_name"]] = (
                f'{cluster["best_platform"]} offers the best price at ${cluster["best_price"]:.0f}; '
                f"average cross-platform price is ${cluster['avg_price']:.0f}."
            )

        return {
            "summary": (
                f'Market intelligence for "{query}" shows {trend}. '
                f"{cheapest['best_platform']} has the strongest headline deal in the current result set."
            ),
            "recommendation": recommendation,
            "market_trend": trend,
            "highlights": highlights,
            "cluster_summaries": cluster_summaries,
            "source": "fallback",
        }
