import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, Request
from typing import List, Dict
import uvicorn
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote

from src.search import router as search_router
from src.years import router as years_router

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

app = FastAPI()
app.include_router(search_router)
app.include_router(years_router)

chats: Dict[str, genai.GenerativeModel] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ip_address = websocket.client.host
    chats[ip_address] = model.start_chat(history=[])
    while True:
        message = await websocket.receive_text()
        if message == "!<FIN>!":
            websocket.close()
            break
        else:
            response = chats[ip_address].send_message(message, stream=True)
            for msg in response:
                await websocket.send_text(msg.text)
            await websocket.send_text("<FIN>")

@app.get("/")
async def read_root():
    return {"message": "API Chat-Rights"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))