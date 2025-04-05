import psutil
from transformers import pipeline

# Function to track memory usage (in MB)
def get_memory_usage():
    process = psutil.Process()  # Get current process
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Convert to MB

# Load the classifier once, outside of the function
classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

def transform_firebase_data(data, event_id):
    """Extracts messages for a specific event ID from Firebase data."""
    if not isinstance(data, dict):
        raise ValueError("Input should be a dictionary with event IDs as keys")
    
    event_messages = data.get(event_id, {})  # Get messages for the given event ID
    return list(event_messages.values()) if isinstance(event_messages, dict) else []

def identify_issues(data, event_id):
    """Identifies crowd-related issues in the given text messages for a specific event ID."""
    
    # Track memory usage before processing
    initial_memory = get_memory_usage()
    print(f"Initial RAM usage: {initial_memory:.2f} MB")
    
    print(f"event_id: {event_id}")
    texts = transform_firebase_data(data, event_id)
    print("texts:", texts)  # Debugging line

    if not texts:
        return []  # Return empty if no messages exist for the event
    
    candidate_labels = [
        "overcrowding", "queue issue", "long waiting time", 
        "poor crowd control", "mismanagement", "slow service"
    ]
    
    # Track memory usage after loading the data
    data_loading_memory = get_memory_usage()
    print(f"RAM usage after data loading: {data_loading_memory:.2f} MB")
    
    # Classify each text in the list
    results = [classifier(text, candidate_labels) for text in texts]

    # Track memory usage after classification
    classification_memory = get_memory_usage()
    print(f"RAM usage after classification: {classification_memory:.2f} MB")
    
    # Collect the labels with high confidence (score > 0.7)
    problems = []
    for res in results:
        if res['scores'][0] > 0.7:  # High confidence labels
            problems.append(res['labels'][0])
    
    # Remove duplicates and return unique issues
    unique_problems = list(set(problems))
    print(f"Identified issues: {unique_problems}")
    
    # Track memory usage after cleanup
    cleanup_memory = get_memory_usage()
    print(f"RAM usage after cleanup: {cleanup_memory:.2f} MB")
    
    return unique_problems

# Example Data (Replace with your Firebase data structure)
data = {
    'event_1': {
        'msg_1': 'The crowd is too large, people are complaining.',
        'msg_2': 'There are long waiting times at the entry points.',
        'msg_3': 'Poor crowd control, people are getting frustrated.',
    },
    'event_2': {
        'msg_1': 'Slow service at the food stalls.'
    }
}

# Example Event ID to analyze
event_id = 'event_1'

# Call the function to identify issues
issues = identify_issues(data, event_id)
print(f"Final identified issues for {event_id}: {issues}")
