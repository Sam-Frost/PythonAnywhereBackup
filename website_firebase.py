import firebase_admin
from firebase_admin import credentials, firestore
import os

service = "mysite/service.json"
service = os.path.join(os.getcwd(), service)

# Initialize Firebase with your credentials
creds = credentials.Certificate(service)
app2 = firebase_admin.initialize_app(creds, name='app2')

# Initialize Firestore
db2 = firestore.client(app=app2)

# Function to save feedback to Firebase
def save_feedback(roll_number, feedback):
    # Reference the "user_feedback" collection in Firestore
    user_feedback_collection = db2.collection("user_feedback")

   # Create a new document with a unique auto-generated ID
    new_feedback_ref, document_id = user_feedback_collection.add({
        "roll_number": roll_number,
        "feedback": feedback
    })

    return "Feedback saved successfully with ID: {}".format(document_id)

from firebase_admin import firestore

# Function to save a user to Firebase
def save_user(name, password):
    # Reference the "users" collection in Firestore
    user_feedback_collection = db2.collection("users")

    # Check if a user with the same roll_number exists
    existing_user = user_feedback_collection.where("roll_number", "==", name).limit(1).get()

    if existing_user:
        # User with the same roll_number already exists, return a message or handle the case as needed
        return "User with this roll_number already exists."

    # If no existing user found, create a new document with a unique auto-generated ID
    new_feedback_ref, document_id = user_feedback_collection.add({
        "roll_number": name,
        "password": password  # Assuming 'password' is the field name for the user's password
    })

    return "User saved successfully with ID: {}".format(document_id)

