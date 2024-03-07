import os
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage

service = "mysite/ServiceAccountKey.json"
service = os.path.join(os.getcwd(), service)

# Initialize Firebase Admin SDK with your credentials JSON file
cred = credentials.Certificate(service)
# Create an app with custom configuration
custom_config = {
    "storageBucket": "campuscompanion-a6bdb.appspot.com"
}

app1 = firebase_admin.initialize_app(cred, name='app1', options=custom_config)

# Reference to your Firestore database
db = firestore.client(app=app1)

def store_data(collection, name, roll_number, email, password, uid):
    try:
        data = {
            'name': name,
            'password': password,
            'roll_number': roll_number,
            'email': email
        }

        # Add the data to a Firestore collection (e.g., 'students')
        db.collection(collection).document(uid).set(data)

        return True  # Data added successfully

    except Exception as e:
        print(f"Error: {str(e)}")
        return False  # Data addition failed


def upload_to_firestore_storage(image_content, rollno):
    # Initialize the storage client
    bucket = storage.bucket()

    # Define the name for the image file and specify the folder path
    folder_path = "profile_pictures/"  # Specify the folder path here
    image_name = folder_path + rollno + ".jpg"

    # Create a blob in Firestore storage
    blob = bucket.blob(image_name)

    # Upload the image content to Firestore storage
    blob.upload_from_string(image_content, content_type='image/jpeg')

    # Get the public URL of the uploaded image
    image_url = blob.public_url
    return image_url

def create_authentication(email, password):
    # Create entry in authentication table
    try:
        # Create a new user with email and password
        user = auth.create_user(
            email=email,
            password=password,
            email_verified=False
        )

        print("Successfully created user: {0}".format(user.uid))
        return user.uid
    except Exception as e:
        print("Error creating user: {0}".format(str(e)))