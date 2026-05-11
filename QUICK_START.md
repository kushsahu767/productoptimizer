# 🚀 Product Price Optimiser - Quick Start Guide

## One-Click Startup (Recommended)

### Windows Users:
Simply **double-click** the `START.bat` file in the project root:
```
productoptimizer/
├── START.bat              ← Double-click this!
├── server.py
└── ...
```

The server will:
1. Start automatically on `http://localhost:3000`
2. Open your browser automatically (or manually visit the URL)
3. Stop with `Ctrl+C` in the terminal

### macOS/Linux Users:
Run the unified server from terminal:
```bash
cd productoptimizer
python3 server.py
```

Then open: `http://localhost:3000`

---

## What's Integrated?

✅ **Frontend** - React app compiled to static files
✅ **Backend** - Flask API server
✅ **Single Port** - Everything runs on port 3000
✅ **Real Product Links** - Amazon and Walmart product pages
✅ **AI Analysis** - Gemini-powered market insights
✅ **Best Deal Button** - One-click to best prices

---

## Features

### 🔍 Smart Search
- Search by product name, brand, or category
- Fuzzy matching for typos
- Automatic clustering of equivalent products

### 💰 Price Comparison
- Real-time prices from Amazon and Walmart
- Best deal highlighted with yellow badge
- Direct links to product pages

### 🤖 AI Insights
- Gemini AI market analysis
- Buy now or wait recommendations
- Price trend insights

### 📊 Search History
- Automatically tracked searches
- Quick access to previous searches

---

## Project Structure

```
productoptimizer/
├── START.bat                 ← Quick start (Windows)
├── server.py                 ← Unified server (frontend + backend)
├── backend/
│   ├── app.py               ← Original Flask app (deprecated)
│   ├── .env                 ← API keys (Gemini, Amazon, Walmart)
│   ├── amazon_service.py
│   ├── walmart_service.py
│   ├── ai_analysis.py
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   ├── dist/                ← Compiled production files
│   └── package.json
├── index.html               ← Entry point (served from dist/)
└── README.md
```

---

## API Endpoints

All endpoints are now under `/api`:

- `GET /api/` - Health check
- `GET /api/search?q=query` - Search products
- `GET /api/history` - Get search history

---

## Configuration

Edit `.env` file in `backend/` to add your API keys:

```
GEMINI_API_KEY=your_key_here
AMAZON_API_KEY=your_key_here
AMAZON_API_URL=https://www.amazon.com/
WALMART_API_URL=http://walmart.com/
```

---

## Troubleshooting

### Port 3000 already in use?
Change the port in `server.py`:
```python
app.run(debug=True, host="127.0.0.1", port=3001)  # Change 3000 to 3001
```

### API not responding?
1. Check if `.env` file has valid API keys
2. Check browser console (F12) for errors
3. Restart the server with `Ctrl+C` and run again

### Search returns no results?
- Ensure API keys are configured in `.env`
- Try searching for: "iphone 14", "nike shoes", "samsung", etc.

---

## Development Mode

If you want to run frontend and backend separately for development:

### Terminal 1 - Backend
```bash
cd backend
python -m pip install -r requirements.txt
python app.py
# Runs on http://localhost:5000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

---

## Production Build

The frontend is already built to `frontend/dist/`. To rebuild:

```bash
cd frontend
npm run build
```

---

## Support

- **Port**: 3000
- **Browser**: http://localhost:3000
- **API Base**: http://localhost:3000/api
- **Stop Server**: `Ctrl+C` in terminal

Enjoy! 🎉
