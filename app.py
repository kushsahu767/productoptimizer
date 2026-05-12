"""Flask API for Product Price Optimiser."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from ai_analysis import GeminiAnalyzer
from amazon_service import AmazonService
from cluster import cluster_products
from data import append_search_history, load_search_history
from preprocess import detect_query_type, extract_attributes
from walmart_service import WalmartService


load_dotenv()

app = Flask(__name__)
CORS(app)

amazon_service = AmazonService()
walmart_service = WalmartService()
gemini_analyzer = GeminiAnalyzer()


def decorate_clusters(clusters: list[dict], ai_payload: dict) -> list[dict]:
    cluster_summaries = ai_payload.get("cluster_summaries", {})
    for cluster in clusters:
        cluster["ai_summary"] = cluster_summaries.get(
            cluster["product_name"],
            f'{cluster["best_platform"]} currently leads at ${cluster["best_price"]:.0f}.',
        )
        cluster["buy_recommendation"] = (
            "Best immediate value"
            if cluster["best_price"] <= cluster["avg_price"]
            else "Monitor for price drop"
        )
    return clusters


@app.get("/")
def healthcheck():
    return jsonify(
        {
            "name": "Product Price Optimiser API",
            "status": "ok",
            "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        }
    )


@app.get("/history")
def history():
    return jsonify({"history": load_search_history()})


@app.get("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    amazon_products = amazon_service.search_products(query)
    walmart_products = walmart_service.search_products(query)
    all_products = amazon_products + walmart_products

    query_type = detect_query_type(query)
    clusters = cluster_products(all_products) if all_products else []
    ai_analysis = gemini_analyzer.analyze_market(query, clusters, query_type)
    decorated_clusters = decorate_clusters(clusters, ai_analysis)
    history_items = append_search_history(query)

    response = {
        "query": query,
        "query_type": query_type,
        "search_context": extract_attributes(query),
        "counts": {
            "amazon": len(amazon_products),
            "walmart": len(walmart_products),
            "clusters": len(decorated_clusters),
        },
        "clusters": decorated_clusters,
        "ai_analysis": ai_analysis,
        "history": history_items,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
