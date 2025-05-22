from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for incoming messages
class Message(BaseModel):
    sender: str
    message: str

# Endpoint to handle chat messages
@app.post("/chat")
async def chat(message: Message):
    try:
        # Send message to Rasa REST API
        rasa_response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": message.sender, "message": message.message}
        )
        rasa_response.raise_for_status()
        responses = rasa_response.json()
        
        # Extract bot responses
        bot_messages = [resp.get("text") for resp in responses if resp.get("text")]
        return {"responses": bot_messages}
    except Exception as e:
        return {"error": str(e)}

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI is running"}

    # rasa run --enable-api -vv --cors "*"
# uvicorn main:app --host 0.0.0.0 --port 8000
# python -m http.server 8001
# uvicorn dash:app --reload --host 0.0.0.0 --port 8000