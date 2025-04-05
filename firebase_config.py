import firebase_admin
from firebase_admin import credentials, db

# Load credentials and initialize Firebase
cred = credentials.Certificate("credentials.json")  # Ensure this file exists
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://kernelforms-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Define a database reference (adjust path as needed)
ref = db.reference('messages')  # Root reference

def get_text_data():
    """Fetches all messages from Firebase."""
    data = ref.get()
    #print("get text was called, data fetched:", data)  # Debugging line
    return data if data else "No data found"

def insert_sample_data():
    """Inserts test data into Firebase."""
    ref.set({
        "event123": {
            "msg1": "The queue is too long",
            "msg2": "Crowd is mismanaged"
        },
        "event456": {
            "msg3": "People are cutting in line"
        }
    })
    print("Sample data inserted!")

def clear_data():
    """Deletes all data under 'messages'."""
    ref.delete()
    print("All data cleared from Firebase!")
