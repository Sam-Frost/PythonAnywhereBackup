import re
from bs4 import BeautifulSoup

import requests

domain = 'ncuindia.edu'

def get_first_word(input):
    words = input.split()  # Split the input string into words using whitespace as a delimiter
    if words:
        return words[0]  # Return the first word
    else:
        return None  # Return None if there are no words in the input


def create_email(name, roll_number, domain):
    roll_number = roll_number.lower()
    name = get_first_word(name)
    # Convert the name to lowercase, remove spaces, and concatenate it with the roll number and domain
    email = f"{name.lower().replace(' ', '')}{roll_number}@{domain}"
    return email

def cleaner(input_string):
    # Remove newline characters and replace with a space
    clean_string = re.sub(r'[\n\r]+', ' ', input_string)

    # Remove extra white spaces (more than one space) with a single space
    clean_string = re.sub(r'\s+', ' ', clean_string).strip()

    return clean_string

def isDate(input_string):
    # Define a regular expression pattern to match the format
    pattern = r'\d{2}-[A-Za-z]+-\d{4}'

    # Use the re.match() function to check if the input matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False

def isDay(input_string):
    # Check if the input string ends with "day"
    if input_string.endswith("day"):
        return True
    else:
        return False

def class_parser(class_string, n):
    # Define a regular expression pattern to extract key-value pairs
    pattern = r'Faculty :- (.*?)\s*Course Code :- (.*?)\s*Room No\. (.*?)\s*Time :- (.*?)$'


    # Use re.search() to find the pattern in the input string
    match = re.search(pattern, class_string)

    # Initialize a dictionary to store the extracted information
    class_info = {}

    if match:
        # Extract and store the values in the dictionary
        class_info['S.No'] = n
        class_info['Faculty'] = match.group(1).strip()
        class_info['Course Code'] = match.group(2).strip()
        class_info['Room No.'] = match.group(3).strip()
        class_info['Time'] = match.group(4).strip()

        # Format the 'Time' value
        class_info['Time'] = class_info['Time'].replace('-', ' - ')

    return class_info

def extract_html_values(html_content):

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the __VIEWSTATE, __VIEWSTATEGENERATOR, and __EVENTVALIDATION input elements by their IDs
    viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
    viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
    eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']

    return {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTVALIDATION': eventvalidation
    }

def get_params(username, password):

    # Define the URL for the POST request
    url = 'https://academics.ncuindia.edu/'  # Replace with the actual URL

    # Define the payload (data) you want to send in the POST request
    payload = {
        'txtUser': username,
        'txtPassword': password
    }

    # Send the POST request and store the response
    response = requests.post(url, json=payload)  # You can also use data= for form data

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            # Try to parse the response as JSON
            response_json = response.json()
        except ValueError:
            data = response.text

            values = extract_html_values(data)

            return values


def leaves_affordable(lectures, present,LOA):
    # Calculate actual lectures by subtracting LOA from total lectures
    actual_lectures = lectures - LOA

    # Calculate attendance percentage
    if actual_lectures > 0:
        attendance_percentage = (present / actual_lectures) * 100
    else:
        attendance_percentage = 0

    classes_skip = 0

    while 70 < attendance_percentage:
        actual_lectures += 1
        attendance_percentage = (present / actual_lectures) * 100
        if 70 < attendance_percentage:
            classes_skip +=1


    return classes_skip

def must_attend_classes(lectures, present,LOA):

    # Calculate actual lectures by subtracting LOA from total lectures
    actual_lectures = lectures - LOA

    # Calculate attendance percentage
    if actual_lectures > 0:
        attendance_percentage = (present / actual_lectures) * 100
    else:
        attendance_percentage = 0

    classes_to_attend = 0

    while attendance_percentage < 70:

        # Increase class to attend by 1
        classes_to_attend += 1
        print("Classes to Attend : ", classes_to_attend)

        # Increase the number of lectures and present by 1
        actual_lectures += 1
        present += 1

        #Re-caluclate the attendancee
        attendance_percentage = (present / actual_lectures) * 100

        print("Attendance : ", attendance_percentage)


    return classes_to_attend

