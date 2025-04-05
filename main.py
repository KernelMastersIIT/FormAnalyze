from fastapi import FastAPI
from firebase_config import get_text_data, db
from model import identify_issues

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is live!"}

@app.get("/analyze/{event_id}")
def analyze(event_id: str):
    """Fetch messages for a specific event and analyze them."""
    texts = get_text_data()
    if not texts:
        return {"error": "No messages found."}
    
    problems = identify_issues(texts, event_id)
    return {"problems": problems}

@app.get("/debug")
def debug():
    """Fetches and returns all stored Firebase data."""
    ref = db.reference('messages')
    data = ref.get()
    if not data:
        return {"error": "No data found in Firebase."}
    return {"firebase_data": data}
