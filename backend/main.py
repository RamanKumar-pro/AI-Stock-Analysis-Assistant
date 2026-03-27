from dotenv import load_dotenv
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

import yfinance as yf

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = ChatOpenAI(
    model = 'c1/openai/gpt-5/v-20250930',
    base_url = 'https://api.thesys.dev/v1/embed/'
)

checkpointer = InMemorySaver()

@tool('get_stock_price', description= "It takes a ticker symbol as input and returns the current stock price for that ticker symbol.")
def get_stock_price(ticker: str) -> str:
    print("get_stock_price called with ticker:", ticker)
    stock = yf.Ticker(ticker)
    return stock.history()['Close'].iloc[-1]

@tool('get_historical_stock_price', description= "It takes a ticker symbol as input and returns the current stock price over time for that ticker symbol on start and end dates.")
def get_historical_stock_price(ticker: str, start_date: str, end_date: str) -> str:
    print("get_historical_stock_price called with ticker:", ticker)
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date).to_dict()

@tool('get_balance_sheet', description= "It takes a ticker symbol as input and returns the balance sheet data for that ticker symbol.")
def get_balance_sheet(ticker: str, year: int) -> str:
    print("get_balance_sheet called with ticker:", ticker)
    stock = yf.Ticker(ticker)
    bs_df = stock.balance_sheet  
    if bs_df is None or bs_df.empty:
        return {}
    if year in bs_df.columns:
        return bs_df[year].to_dict()
    latest = bs_df.columns[-1]
    return bs_df[latest].to_dict()

@tool('get_stock_news', description= "It takes a ticker symbol as input and returns the latest news for that ticker symbol.")
def get_stock_news(ticker: str) -> str:
    print("get_stock_news called with ticker:", ticker)
    stock = yf.Ticker(ticker)
    return stock.news

agent = create_agent(
    model = model,
    checkpointer = checkpointer,
    tools = [get_stock_price, get_historical_stock_price, get_balance_sheet, get_stock_news]
)

class PromptObject(BaseModel):
    content: str
    id: str
    role: str

class RequestObject(BaseModel):
    prompt:  PromptObject
    threadId: str
    responseId: str

@app.post('/api/chat')
async def chat(request: RequestObject):
    config = {'configurable': {'thread_id': request.threadId}}

    def generate():
        for token, _ in agent.stream(
            {'messages': [
                SystemMessage('You are a stock analysis assistant. You have the ability to get real-time stock prices, historical stock prices (given a date range), news and balance sheet data for a given ticker symbol.'),
                HumanMessage(request.prompt.content)
            ]},
            stream_mode = 'messages',
            config = config
        ):
            yield token.content
    
    return StreamingResponse(generate(), media_type = 'text/event-stream',
                             headers= {'Cache-Control': 'no-cache, no-transform',
                                      'Connection': 'keep-alive'
                             })

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port= 8888)

