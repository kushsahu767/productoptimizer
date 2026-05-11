# Product Price Optimiser

Product Price Optimiser is a startup-style AI-powered ecommerce comparison platform that searches products across Amazon and Walmart, clusters equivalent items with fuzzy matching, and generates buying guidance with Gemini-ready market analysis.

## Highlights

- Cross-platform product search from Amazon and Walmart service layers
- Title normalization with brand/model/storage extraction
- `rapidfuzz.token_sort_ratio`-based similarity scoring
- Greedy clustering with brand validation and representative selection
- Best deal and best value detection per cluster
- Gemini AI integration with resilient local fallback summaries
- Modern React + Tailwind frontend inspired by SaaS pricing intelligence dashboards
- Search history, brand filters, sorting, loading states, and dark mode

## Project Structure

```text
backend/
├── app.py
├── matcher.py
├── cluster.py
├── ai_analysis.py
├── amazon_service.py
├── walmart_service.py
├── preprocess.py
├── data.py
├── requirements.txt
├── .env
└── .env.example

frontend/
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── vite.config.js
├── .env.example
└── src/
    ├── components/
    ├── pages/
    ├── services/
    ├── utils/
    ├── App.js
    ├── main.js
    └── index.css
```

## Backend Architecture

### 1. Preprocessing

- Normalizes titles by lowering case, removing special characters, collapsing whitespace, and dropping noisy stopwords
- Extracts brand, model, storage, and keyword features for stronger matching
- Detects whether the search is category-oriented or product-specific

### 2. Fuzzy Matching

`matcher.py` combines:

- `rapidfuzz.fuzz.token_sort_ratio`
- `rapidfuzz.fuzz.partial_ratio`
- brand bonus / mismatch penalty
- storage match bonus
- keyword overlap bonus

This keeps the algorithm close to the requirement while making false matches less likely.

### 3. Greedy Clustering

`cluster.py` implements the required greedy clustering flow:

1. Loop through products
2. Compare each product with each cluster representative
3. If similarity is at least `75` and brands match, add to that cluster
4. Otherwise create a new cluster

The representative is re-selected from cluster members using title quality, price, and rating signals.

### 4. AI Analysis

`ai_analysis.py` supports two modes:

- Live Gemini mode when `GEMINI_API_KEY` is configured
- Fallback deterministic insight generation when no key is available

## Frontend Experience

- Hero landing page with live-search workflow
- Search results workspace with:
  - AI insight panel
  - filter sidebar
  - sort dropdown
  - cluster cards
  - deal badges
  - external platform links
- Responsive layout for desktop, tablet, and mobile
- Dark mode toggle and local search history

## API

### `GET /search?q=iphone 14`

Returns:

```json
{
  "query": "iphone 14",
  "query_type": "specific",
  "counts": {
    "amazon": 2,
    "walmart": 1,
    "clusters": 1
  },
  "clusters": [
    {
      "product_name": "Apple iPhone 14 128GB Blue",
      "best_platform": "Amazon",
      "best_price": 699.0,
      "items": []
    }
  ],
  "ai_analysis": {
    "summary": "Market intelligence summary",
    "recommendation": "buy now"
  }
}
```

### `GET /history`

Returns the latest search history persisted in lightweight JSON storage.

## Environment Variables

### Backend `.env`

```env
GEMINI_API_KEY=
AMAZON_API_KEY=
WALMART_API_KEY=
AMAZON_API_URL=
WALMART_API_URL=
```

### Frontend `.env`

```env
VITE_API_BASE_URL=http://localhost:5000
```

## Setup Instructions

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The Flask API starts on `http://localhost:5000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite app starts on `http://localhost:5173`.

## Swapping Mock Data for Real APIs

The Amazon and Walmart services are already split into dedicated modules. To connect production APIs:

1. Fill in `AMAZON_API_KEY`, `WALMART_API_KEY`, and endpoint URLs.
2. Adjust each service's `_fetch_live()` request shape to match the real provider.
3. Keep the response normalized to:

```json
{
  "title": "",
  "price": 0,
  "platform": "",
  "rating": 0,
  "image": "",
  "link": "",
  "brand": ""
}
```

The current fallback dataset includes 20+ listings spanning Apple, Samsung, Nike, Adidas, Sony, and Asus, with intentionally varied naming for realistic clustering.

## Suggested Demo Queries

- `iphone 14`
- `nike shoes`
- `gaming laptop`
- `smartwatch`
- `sony headphones`
- `samsung`

## Notes

- The project uses JSON mock storage for search history to keep local setup easy.
- Gemini analysis is optional and gracefully falls back when no API key is configured.
- The UI design follows the supplied visual reference while extending it into a full two-page product experience.
