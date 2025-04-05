from transformers import pipeline 

classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

def transform_firebase_data(data, event_id):
    """Extracts messages for a specific event ID from Firebase data."""
    if not isinstance(data, dict):
        raise ValueError("Input should be a dictionary with event IDs as keys")
    
    event_messages = data.get(event_id, {})  # Get messages for the given event ID
    return list(event_messages.values()) if isinstance(event_messages, dict) else []

def identify_issues(data, event_id):
    """Identifies crowd-related issues in the given text messages for a specific event ID."""
    print(f"event_id: {event_id}")
    texts = transform_firebase_data(data, event_id)
    print("texts:", texts)  # Debugging line

    if not texts:
        return []  # Return empty if no messages exist for the event
    
    candidate_labels = [
        "overcrowding", "queue issue", "long waiting time", 
        "poor crowd control", "mismanagement", "slow service"
    ]
    
    results = [classifier(text, candidate_labels) for text in texts]
    problems = [res['labels'][0] for res in results if res['scores'][0] > 0.7]  # High confidence labels
    
    return list(set(problems))  # Remove duplicates