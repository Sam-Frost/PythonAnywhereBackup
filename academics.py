import json
import requests # Login into page, send and get requests
from bs4 import BeautifulSoup # Parse through HTMl response
from urllib.parse import urljoin
import re # Required for cleaner
import pandas as pd # Create dataframe and store data
from firebase import upload_to_firestore_storage # Create dataframe and store data

from helper import class_parser, cleaner, get_params, isDate, isDay

login_url = ("https://academics.ncuindia.edu/Login.aspx")
loggedin_url = ("https://academics.ncuindia.edu/Student/Dashboard.aspx")
attendace = ('https://academics.ncuindia.edu/Student/AttendanceSummary.aspx')

def create_payload(username, password):

    values = get_params(username, password)

    payload = {
    '__VIEWSTATE' : values['__VIEWSTATE'],
    '__VIEWSTATEGENERATOR' : values['__VIEWSTATEGENERATOR'],
    '__EVENTVALIDATION' : values['__EVENTVALIDATION'],
    'rdSelect' : 'Staff',
    'txtUser' : username,
    'txtPassword' : password,
    'btnlogin' : 'Login'
    }

    return payload

def get_attendance(username, password):
    # Create a session so that the login stays
    with requests.session() as s:

        payload = create_payload(username, password)

        #Logging in to the website
        response_login = s.post(login_url, data=payload)

        #Requeting attendace page
        response_attendace = s.get(attendace)

        #Parsing the repsonse for the html page
        soup = BeautifulSoup(response_attendace.content, 'html.parser')
        table = soup.table

        headers = table.find_all('th')
        titles = []
        for item in headers:
            titles.append(cleaner(item.text))

        rows = table.find_all('tr')

        df = pd.DataFrame(columns=titles)

        for i in rows[1:]:

            # Get all td elements
            data = i.find_all('td')

            row = [cleaner(tr.text) for tr in data]

            # Skip the aggregate row in the webpage
            if row[1] == "Aggregate (%)":
                continue

            # Add data to the dataframe
            l = len(df)
            df.loc[l] = row

        return df.to_json(orient='records')



def get_timetable(username, password):

    # Create a session so that the login stays
    with requests.session() as s:

        payload = create_payload(username, password)

        timetable = []

        #Logging in to the website
        response_login = s.post(login_url, data=payload)

        #Parsing the repsonse for the html page
        soup = BeautifulSoup(response_login.content, 'html.parser')

        rows = soup.find_all('tr') # Find all rows in the table

        flag = True # Flag to skip the table head in the loop

        # Iterate through the rows and extract data
        for row in rows:

            n = 1 # Set serial number of each class for oderly printing in app

            # Skippig table head
            if flag:
                flag = False
                continue


            row_dict = {'Day' : '',
                        'Date' : '',
                        'Lecture Details' : []}

            # Find all cells in the row
            cells = row.find_all('td')

            # Extract and print data from each cell
            for cell in cells:
                text = cell.text.strip()
                if(isDay(text)):
                    row_dict['Day'] = text
                elif(isDate(text)):
                    row_dict['Date'] = text
                else :
                    row_dict['Lecture Details'].append(class_parser(text, n))
                    n += 1

            timetable.append(row_dict)
            print(json.dumps(row_dict, indent=4))
            # Print a separator for better readability
            print("-" * 40)  # You can adjust the number of dashes as needed

        return json.dumps(timetable)


def get_name(username, password):
    url = "https://academics.ncuindia.edu/Login.aspx"

    with requests.session() as s:

        payload = create_payload(username, password)

        #Logging in to the website
        response_login = s.post(url, data=payload)

        #Parsing the repsonse for the html page
        soup = BeautifulSoup(response_login.content, 'html.parser')

        element = soup.find(id='lblRegNo')

        if element:
            element_text = element.text
            return element_text.title()
        else:
            print("Element not found.")


def store_profile_pic(username, password):
    base_url = "https://academics.ncuindia.edu/"

    with requests.session() as s:
        payload = create_payload(username, password)

        # Logging in to the website
        response_login = s.post(urljoin(base_url, "Login.aspx"), data=payload)

        # Parsing the response for the HTML page
        soup = BeautifulSoup(response_login.content, 'html.parser')

        # Find the input tag with the specified attributes
        img_tag = soup.find('input', {'type': 'image', 'name': 'ctl00$imgStudent1', 'id': 'imgStudent1'})

        if img_tag:
            # Extract the image source URL from the 'src' attribute
            image_url = urljoin(base_url, img_tag['src'])

            # Send a GET request to the image URL
            image_response = s.get(image_url)

            if image_response.status_code == 200:
                # Save the image to a local file
                # with open('downloaded_image.jpg', 'wb') as file:
                #     file.write(image_response.content)
                # print('Image downloaded successfully and saved as "downloaded_image.jpg".')

                # Upload the image content to Firestore storage
                image_url = upload_to_firestore_storage(image_response.content, username)
                print('Image uploaded to Firestore storage with URL:', image_url)

            else:
                print('Failed to download the image.')
        else:
            print('Image tag not found on the page.')





