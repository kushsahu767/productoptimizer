"""Unified server for Product Price Optimiser - Frontend + Backend in one."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.ai_analysis import GeminiAnalyzer
from backend.amazon_service import AmazonService
from backend.cluster import cluster_products
from backend.data import append_search_history, load_search_history
from backend.preprocess import detect_query_type, extract_attributes
from backend.walmart_service import WalmartService

load_dotenv(Path(__file__).parent / "backend" / ".env")

app = Flask(__name__, static_folder="frontend/dist", static_url_path="/")
CORS(app)

# Initialize services
amazon_service = AmazonService()
walmart_service = WalmartService()
gemini_analyzer = GeminiAnalyzer()


def decorate_clusters(clusters: list[dict], ai_payload: dict) -> list[dict]:
    """Add AI summaries and recommendations to clusters."""
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


# ============================================================================
# API ROUTES
# ============================================================================


@app.get("/api/")
def healthcheck():
    """Health check endpoint."""
    return jsonify(
        {
            "name": "Product Price Optimiser API",
            "status": "ok",
            "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        }
    )


@app.get("/api/history")
def history():
    """Get search history."""
    return jsonify({"history": load_search_history()})


@app.get("/api/search")
def search():
    """Search products across platforms."""
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


# ============================================================================
# FRONTEND ROUTES
# ============================================================================


@app.route("/")
def index():
    """Serve index.html for root path."""
    return send_from_directory("frontend/dist", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    """Serve static files (CSS, JS, images, etc)."""
    if path and Path(f"frontend/dist/{path}").is_file():
        return send_from_directory("frontend/dist", path)
    # For client-side routing, return index.html
    return send_from_directory("frontend/dist", "index.html")


# ============================================================================
# STARTUP
# ============================================================================


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🚀 Product Price Optimiser - Unified Server")
    print("=" * 70)
    print(f"  Frontend: http://localhost:3000")
    print(f"  API Base: http://localhost:3000/api")
    print(f"  Status: Running...")
    print("=" * 70 + "\n")

    app.run(debug=True, host="127.0.0.1", port=3000, use_reloader=False)
