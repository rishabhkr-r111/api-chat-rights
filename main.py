import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from typing import List, Dict
import uvicorn

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        print(message)
        if message == "!<FIN>!":
                websocket.close()
                break
        else:
            response = chat.send_message(message, stream=True)
            for msg in response:
                await websocket.send_text(msg.text)
            await websocket.send_text("<FIN>")

@app.get("/")
async def read_root():
    return {"message": "API Chat-Rights"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))