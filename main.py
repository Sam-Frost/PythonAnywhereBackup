from website_firebase import save_feedback, save_user
from academics import get_attendance, get_name, get_timetable
from flask import Flask, request, render_template, session, redirect, url_for
from backend import calculate_leaves_and_must_attend, register_user
import json
from functools import wraps
import os

# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)



app = Flask(__name__)

# Generate a secure random secret key
secret_key = os.urandom(24)

# Convert the secret key to a string in hexadecimal format
secret_key_hex = secret_key.hex()

app.secret_key = secret_key_hex  # Replace with your secret key

# Simulated user data (you would typically store this in a database)
users = {
    'user1': {'username': '20CSU093', 'password': 'QRjFyqJp'},
    'user2': {'username': '20CSU159', 'password': 'k2Q0jn8E'},
}

# Custom decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function



# Welcome message for homepage
@app.route('/')
def index():
    return 'The web server is running!!!!'

# Welcome message for homepage
@app.route('/testing')
def testing():
    return 'The web server is testing!!!!'


'''
    API ENDPOINTS
'''

# API endpoint to retrieve attendance
@app.route('/attendance', methods=['POST'])
def attendance():
    data = request.get_json()
    return get_attendance(data['username'], data['password'])

# API endpoint to retrieve timetable
@app.route('/timetable', methods=['POST'])
def timetable():
    data = request.get_json()
    return get_timetable(data['username'], data['password'])

# API endpoint to register user timetable
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if register_user(data['username'], data['password']) :
        return "Data added succesfully"
    else :
        return "Error in adding data!"


'''
    Web Application ENDPOINTS
'''

roll_number=''
password=''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else :

        # Get the submitted form data
        roll_number = request.form.get('roll_number')
        password = request.form.get('password')

        session['logged_in'] = True
        session['username'] = roll_number
        session['password'] = password
        return redirect(url_for('ncuAttendance'))

@app.route("/logout")
def logout():
    session['username'] = None
    session['password'] = None
    return redirect("/login")

@app.route('/ncu/attendance', methods=['GET'])
@login_required
def ncuAttendance():
    if request.method == 'GET':
        roll_number = session['username']
        password = session['password']
        data = get_attendance(roll_number, password)
        data = json.loads(data)
        data = calculate_leaves_and_must_attend(data)
        username = get_name(roll_number, password)
        save_user(session['username'], session['password'])
        return render_template('attendance.html', data=data, namee=username)

@app.route('/ncu/timetable', methods=['GET','POST'])
@login_required
def ncuTimetable():
    return render_template('timetable.html')

@app.route('/ncu/feedback', methods=['GET','POST'])
@login_required
def feedback():
    if request.method == 'POST':
        data = request.form.get('feedback')
        response  = save_feedback(session['username'] ,data)
        print(response)
        return render_template('feedback_success.html')

    else :
        return render_template('feedback.html')

@app.route('/ncu/about', methods=['GET','POST'])
@login_required
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
