# Advanced AI Stock Analysis Assistant - Backend

## Overview

FastAPI backend with LangChain/LangGraph agent for stock data tools using yfinance.

Endpoints:

- POST `/api/chat`  
  payload: `{ "prompt":{...}, "threadId":"...", "responseId":"..." }`

Tools:

- `get_stock_price(ticker)`
- `get_historical_stock_price(ticker,start_date,end_date)`
- `get_balance_sheet(ticker,year)`
- `get_stock_news(ticker)`

## Prerequisites

- Python 3.10+
- [uv](https://github.com/ubernostrum/uv)
- Node/Vite for frontend

## Setup

```powershell
cd d:\Programming\Projects\Advanced AI Stock Analysis Assistant\backend
uv venv .venv
.venv\Scripts\Activate.ps1
uv sync
```

If you need pip:

```powershell
pip install -r requirements.txt
```

## Environment

Create `.env` from `.env.example`:

```text
OPENAI_API_KEY=your_api_key_here
```

## Run

```powershell
uv run main.py
```

Open <http://localhost:8888>

## Notes

- CORS is already configured for Vite localhost ports.
- `yfinance.Ticker(...).news` is property (no `()`).
- `yfinance.Ticker(...).balance_sheet` is DataFrame (not callable).
