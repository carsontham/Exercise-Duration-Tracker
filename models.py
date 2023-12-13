import pymongo
from datetime import datetime

connection = pymongo.MongoClient('mongodb://localhost:27017')
db = connection['ECA']

def read_All_appUser():
    return db.appUser.find({})

def read_appUser(email_id):
    assert email_id is not None 
    return db.appUser.find_one({'email_id': email_id})

def create_appUser(email_id, password, gender, weight, height, DoB):
    assert email_id is not None
    assert password is not None
    assert gender is not None
    assert weight is not None
    assert height is not None
    assert DoB is not None

    db.appUser.insert_one({'email_id': email_id, 'password': password, 'gender': gender, 'weight': weight, 'height': height, 'DoB': DoB})

def create_calorie_log(email_id, datetime, calorie):
    assert email_id is not None
    assert datetime is not None
    assert calorie is not None
    
    db.calorieLog.insert_one({'email_id':email_id, 'datetime': datetime, 'calorie': calorie})

def create_log(email_id, datetime, weight, walking, running, swimming, bicycling): 
    assert email_id is not None
    assert datetime is not None
    assert weight is not None
    assert walking is not None
    assert running is not None
    assert swimming is not None
    assert bicycling is not None

    db.log.insert_one({'email_id':email_id, 'datetime': datetime, 'weight':weight,\
        'walking':walking, 'running':running, 'swimming':swimming, 'bicycling':bicycling })

def read_current_user_calorieLog(email_id):
    calorieLogs = []
    for calorieLog in db.calorieLog.find():
        if calorieLog['email_id'] == email_id:
            calorieLogs.append ({
                        "email_id" : calorieLog['email_id'],
                        "datetime" : datetime.strftime(calorieLog['datetime'], '%Y-%m-%dT%H:%M'),
                        "calorie" : calorieLog["calorie"]
                        })
    print (calorieLogs)
    return calorieLogs

def read_all_calorieLog():
    calorieLogs = []
    for calorieLog in db.calorieLog.find():
        calorieLogs.append ({
                        "email_id" : calorieLog['email_id'],
                        "datetime" : datetime.strftime(calorieLog['datetime'], '%Y-%m-%dT%H:%M'),
                        "calorie" : calorieLog["calorie"]
                        })
    print (calorieLogs)
    return calorieLogs
