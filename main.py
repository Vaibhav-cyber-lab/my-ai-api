import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI(title="My AI API", version="1.0")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MY_API_KEY = os.getenv("MY_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=GEMINI_API_KEY)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "My AI API is running"
    }


@app.post("/v1/chat")
def chat(
    request: ChatRequest,
    authorization: str | None = Header(default=None)
):

    if authorization != f"Bearer {MY_API_KEY}":
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=request.message
    )

    return {
        "response": response.text
    }
