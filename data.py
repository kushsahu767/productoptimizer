"""Sample product data and lightweight JSON storage helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
SEARCH_HISTORY_PATH = BASE_DIR / "search_history.json"


SAMPLE_PRODUCTS = {
    "amazon": [
        {
            "title": "Apple iPhone 14 128GB Blue",
            "price": 699.0,
            "platform": "Amazon",
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1678911820864-e8f8d4d9cf4e?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/Apple-iPhone-128GB-Unlocked-Latest/dp/B0B8BLVW9B",
            "brand": "Apple",
        },
        {
            "title": "Apple iPhone 14 (128 GB) - Blue",
            "price": 724.0,
            "platform": "Amazon",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1678911820864-e8f8d4d9cf4e?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/s?k=iPhone+14+128GB+blue",
            "brand": "Apple",
        },
        {
            "title": "Samsung Galaxy S23 128GB Phantom Black",
            "price": 649.0,
            "platform": "Amazon",
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/SAMSUNG-Galaxy-Unlocked-Smartphone-Phantom/dp/B0BP8FDVBJ",
            "brand": "Samsung",
        },
        {
            "title": "Nike Air Max 270 Men's Running Shoes White",
            "price": 89.0,
            "platform": "Amazon",
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/s?k=Nike+Air+Max+270+white",
            "brand": "Nike",
        },
        {
            "title": "Nike Air Zoom Pegasus 40 Men's Running Shoes",
            "price": 95.0,
            "platform": "Amazon",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1543508282-6319a3e2621f?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/s?k=Nike+Air+Zoom+Pegasus+40",
            "brand": "Nike",
        },
        {
            "title": "Nike React Infinity Run 3 Running Shoe",
            "price": 129.0,
            "platform": "Amazon",
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/s?k=Nike+React+Infinity+Run+3",
            "brand": "Nike",
        },
        {
            "title": "Adidas Ultraboost Light Men's Sneakers",
            "price": 142.0,
            "platform": "Amazon",
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/s?k=Adidas+Ultraboost+Light",
            "brand": "Adidas",
        },
        {
            "title": "Sony WH-1000XM5 Noise Cancelling Headphones Black",
            "price": 329.0,
            "platform": "Amazon",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/Sony-WH-1000XM5-Canceling-Headphones-phone-call/dp/B09LH7FHXY",
            "brand": "Sony",
        },
        {
            "title": "Sony PlayStation 5 Console Slim Edition",
            "price": 499.0,
            "platform": "Amazon",
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/s?k=PlayStation+5+Slim+console",
            "brand": "Sony",
        },
        {
            "title": "Apple Watch Series 9 GPS 45mm Midnight",
            "price": 379.0,
            "platform": "Amazon",
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1579586337278-3f436f25d4d6?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/Apple-Watch-Series-Midnight-Fitness/dp/B0CCZ8RDXL",
            "brand": "Apple",
        },
        {
            "title": "ASUS ROG Strix G16 Gaming Laptop RTX 4060",
            "price": 1399.0,
            "platform": "Amazon",
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.amazon.com/s?k=ASUS+ROG+Strix+G16+RTX+4060",
            "brand": "Asus",
        },
    ],
    "walmart": [
        {
            "title": "iPhone 14 by Apple 128GB Blue Unlocked",
            "price": 712.0,
            "platform": "Walmart",
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1678911820864-e8f8d4d9cf4e?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/ip/Apple-iPhone-14-128GB-Blue-Unlocked/429505128",
            "brand": "Apple",
        },
        {
            "title": "Samsung Galaxy S23 Smartphone 128 GB Black",
            "price": 662.0,
            "platform": "Walmart",
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Samsung+Galaxy+S23+128GB",
            "brand": "Samsung",
        },
        {
            "title": "Nike Air Max 270 Men's Shoe White",
            "price": 105.0,
            "platform": "Walmart",
            "rating": 4.3,
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Nike+Air+Max+270",
            "brand": "Nike",
        },
        {
            "title": "Nike Zoom Pegasus 40 Men's Shoes",
            "price": 110.0,
            "platform": "Walmart",
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1543508282-6319a3e2621f?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Nike+Zoom+Pegasus+40",
            "brand": "Nike",
        },
        {
            "title": "Nike React Infinity Run Flyknit 3 Men",
            "price": 119.0,
            "platform": "Walmart",
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Nike+React+Infinity+Run",
            "brand": "Nike",
        },
        {
            "title": "Adidas Ultraboost Light Running Sneaker Men",
            "price": 149.0,
            "platform": "Walmart",
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Adidas+Ultraboost+Light",
            "brand": "Adidas",
        },
        {
            "title": "Sony WH1000XM5 Wireless Noise Canceling Headphones",
            "price": 348.0,
            "platform": "Walmart",
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Sony+WH1000XM5",
            "brand": "Sony",
        },
        {
            "title": "Sony PlayStation 5 Slim Gaming Console",
            "price": 519.0,
            "platform": "Walmart",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=PlayStation+5+Slim",
            "brand": "Sony",
        },
        {
            "title": "Apple Watch Series 9 GPS Smartwatch 45mm",
            "price": 399.0,
            "platform": "Walmart",
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1579586337278-3f436f25d4d6?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Apple+Watch+Series+9",
            "brand": "Apple",
        },
        {
            "title": "ASUS ROG Strix G16 Gaming Laptop Core i7 RTX4060",
            "price": 1449.0,
            "platform": "Walmart",
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=ASUS+ROG+Strix+G16",
            "brand": "Asus",
        },
        {
            "title": "Samsung Galaxy Watch 6 Bluetooth 44mm",
            "price": 255.0,
            "platform": "Walmart",
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=900&q=80",
            "link": "https://www.walmart.com/search/?query=Samsung+Galaxy+Watch+6",
            "brand": "Samsung",
        },
    ],
}


def load_search_history() -> list[str]:
    if not SEARCH_HISTORY_PATH.exists():
        return []

    try:
        return json.loads(SEARCH_HISTORY_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_search_history(history: list[str]) -> None:
    SEARCH_HISTORY_PATH.write_text(json.dumps(history[:8], indent=2), encoding="utf-8")


def append_search_history(query: str) -> list[str]:
    cleaned = query.strip()
    if not cleaned:
        return load_search_history()

    history = [item for item in load_search_history() if item.lower() != cleaned.lower()]
    history.insert(0, cleaned)
    save_search_history(history)
    return history[:8]


def as_serializable(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {key: as_serializable(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [as_serializable(item) for item in payload]
    return payload
