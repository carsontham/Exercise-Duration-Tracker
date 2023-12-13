from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from markupsafe import escape
from flask_cors import CORS
from datetime import datetime
import models
import csv

app = Flask(__name__)
CORS(app)

import auth

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_email = models.read_appUser(email) 

        if user_email is not None: #check if email id exist
            stored_hashed_password = user_email['password']
            bcrypt = Bcrypt()
            if bcrypt.check_password_hash(stored_hashed_password, password):
#            if user_email['password'] == password: # password is correct
                flash(f'Log in successful. Welcome {email}!')
                auth.userLogin(email)
                return render_template('log.html')
            else:
                flash(f'Please check your login details and try again.') #password is wrong
                return render_template('index.html')
        else:
            flash(f'Email user {email} does not exist. Please register first.')
            return render_template('index.html')
        

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        height = request.form.get('height')
        DoB = request.form.get('DoB')

        user_email = models.read_appUser(email) ## TO CHECK FOR EXISTING EMAIL_ID
        
        if user_email is not None:
            flash(f'Email address {email} already exist! Try again.')
            return render_template('register.html')
        else:
            bcrypt = Bcrypt()
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            models.create_appUser(email, hashed_password, gender, weight, height, DoB) #CREATE NEW USER IN DATABASE
            flash(f'New user {email} created! Please login')
            print(f'New Register: Login email is {email}, Password is {password}, Gender is {gender}, Weight is {weight}, Height is {height}, Date of Birth is {DoB}')
            return redirect(url_for('login'))

@app.route('/log', methods = ['GET', 'POST'])
@auth.login_required
def log():
    if request.method == 'GET':
        return render_template('log.html')

    elif request.method == 'POST':
        datetime_str = request.form.get('datetime')
        weight = request.form.get('weight')
        walking = request.form.get('walking')
        running = request.form.get('running')
        swimming = request.form.get('swimming')
        bicycling = request.form.get('bicycling')

        weight_float = float(weight)
        walking_float = float(walking)
        running_float = float(running)
        swimming_float = float(swimming)
        bicycling_float = float(bicycling)

        datetimeObj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M') #convert to datetime object

##############################################################################################
################ THE CODES BELOW IS TO CALCULATE BMR DEPENDING ON THE USER INFO ##############
##############################################################################################

        email_id = auth.current_user.get_id() ### TO GET CURRENTLY LOGGED-IN USER EMAIL_ID

        user_details = models.read_appUser(email_id) ### INFO OF LOGGED-IN USER RETRIEVED FROM DATABASE
        
        height_float = float(user_details['height']) # User Heigh
        DoB = datetime.strptime(user_details['DoB'], '%Y-%m-%d') # User Date of Birth
        gender = user_details['gender'] # get gender

        timeNow = datetime.today() # get time NOW
        age = timeNow.year - DoB.year #get age NOW

        userBMR = getUserBMR(weight_float, height_float, age, gender) #calculate admin BMR, weight_float is from input
        
        ###### totalCalories is calculated using inputs from Log.html page as well as  BMR of Admin
        totalCalories_float = getTotalCalories(weight_float, walking_float, running_float, swimming_float, bicycling_float, userBMR)
        totalCalories_str = str(totalCalories_float)

        models.create_log(email_id, datetimeObj, weight_float, walking_float, running_float, swimming_float, bicycling_float)
        models.create_calorie_log(email_id, datetimeObj, totalCalories_float) #total calories saved in calorie_log collection

        return jsonify({'cal' : totalCalories_str})
        #return render_template('dashboard.html')

@app.route('/upload', methods = ('GET', 'POST'))
@auth.login_required
def upload():
    if request.method == 'GET':
        if auth.current_user.get_id() == 'admin@fitwell.com':
            return render_template('upload.html')
        else:
            flash(f'You are not authorized!')
            flash(f'You have been signed out due to suspicious activity!')
            auth.userLogout()
            return render_template('index.html')

    elif request.method == 'POST':
        if request.files:
            uploadedFile = request.files['csvfile']
            f = uploadedFile.filename
            uploadedFile.save(f)
            print('Uploaded File has been saved')

        with open(f, 'r', encoding= 'utf-8-sig') as f:
            data = csv.reader(f, delimiter = ",")
            for i in data:
                weight_float = float(i[2])
                walking_float = float(i[3])
                running_float = float(i[4])
                swimming_float = float(i[5])
                bicycling_float = float(i[6])

                datetimeObj = datetime.strptime(i[1], '%Y-%m-%dT%H:%M')

                email_id = i[0]
                user_email = models.read_appUser(email_id) 
                height_float = float(user_email['height']) # user height
                DoB = datetime.strptime(user_email['DoB'], '%Y-%m-%d') # user Date of Birth
                timeNow = datetime.today() # get time NOW
                age = timeNow.year - DoB.year #get user age
                gender = user_email['gender'] # get user gender 
                userBMR = getUserBMR(weight_float, height_float, age, gender) #calculate admin BMR, weight_float is from input
        
                ###### totalCalories is calculated using inputs from Log.html page as well as BMR of Admin
                totalCalories_float = getTotalCalories(weight_float, walking_float, running_float, swimming_float, bicycling_float, userBMR)
                totalCalories_str = str(totalCalories_float)

                models.create_log(email_id, datetimeObj, weight_float, walking_float, running_float, swimming_float, bicycling_float)
                models.create_calorie_log(email_id, datetimeObj, totalCalories_float) #total calories saved in calorie_log collection
            return render_template('dashboard.html')

@app.route('/api/calorieLog')
@auth.login_required
def calorieLog():
    calorieLogs = []
    user_id = auth.current_user.get_id()
    if user_id == 'admin@fitwell.com':
        ### IF LOGGED-IN USER IS ADMIN, RETRIEVE ALL DATA FROM DATABASE
        ### IDEA IS TO GET ALL LOGGED DATA OF ALL REGISTERED USERS
        ### WHEN DOING D3 CHART, MULTPLE GRAPHS WILL BE DRAWN BASED ON EMAIL_ID
        ### TO DISTINCT OUT THE VARIOUS USERS AND DISPLAY DIFFERENT GRAPHS
        calorieLogs = models.read_all_calorieLog()
        return jsonify({'calorieLogs' : calorieLogs})

    else:
        calorieLogs = models.read_current_user_calorieLog(user_id) 
        ### ONLY RETRIEVE LOGGED-IN USER DATA
        ### for displaying of logged-in user calorie graph
        return jsonify({'calorieLogs' : calorieLogs})

@app.route('/dashboard', methods = ('GET', 'POST'))
@auth.login_required
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')

import mail

@app.route('/feedback', methods = ['GET', 'POST'])
@auth.login_required
def feedback():
    if request.method == 'GET':
        return render_template('feedback.html')

    elif (request.method == 'POST'):
        email = auth.current_user.get_id()
        print(email)
        mail.send_mail('Feedback Received', email ,'Your feedback has been received. Please allow us to get back to you.')
        flash('Thank you for your feedback')
        return redirect(url_for('feedback'))


@app.route('/logout')
@auth.login_required
def logout():
    auth.userLogout()
    return render_template('index.html')

def getTotalCalories(weight, walking, running, swimming, bicycling, userBMR): ###TOTAL CALORIES OF ACTIVITY AND BMR
    totalCalories = (walking * 0.084 * weight) + (running * 0.21 * weight) + (swimming * 0.13 * weight) + (bicycling * 0.064 * weight) + userBMR
    return totalCalories

def getUserBMR(weight_float, height_float, age, gender): ###CALCULATE BMR
    if gender == 'M':
        userBMR = 88.362 + (13.397*weight_float) + (4.799 * height_float) - (5.677 * age)
    
    else:
        userBMR = 447.593 + (9.247*weight_float) + (3.098* height_float) - (4.330 * age)

    return userBMR
