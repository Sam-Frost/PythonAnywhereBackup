from academics import get_name, store_profile_pic
from firebase import create_authentication, store_data
from helper import create_email, leaves_affordable, must_attend_classes

domain = 'ncuindia.edu'

# Profile pic, dob to be added
def register_user(username, password):
    
    # Get names from academics portal
    name = get_name(username, password)
    print(name)
    
    # Create the email based on username and roll number
    email = create_email(name, username, domain)
    print(email)
    
    # Create entry in the authentication table and send verfication mail
    uid = create_authentication(email, password)

    store_profile_pic(username, password)

    # Store the data in firebase
    if store_data("testing", name, username, email, password, uid):
        return True
    else :
        return False
    
def calculate_leaves_and_must_attend(data):
    for entry in data:
        lectures = int(entry['Total Lecture'])
        present = int(entry['Total Present'])
        LOA = int(entry['Leave of Absence'])
        
        entry['Leaves Affordable'] = leaves_affordable(lectures, present, LOA)
        entry['Must Attend Class'] = must_attend_classes(lectures, present, LOA)
    
    return data    
    


