#db >repository > login.py
from sqlalchemy import or_
from sqlalchemy.orm import Session

from db.models.users import User 
import requests
import json
import os
from dotenv import load_dotenv

pin_id = {}
load_dotenv()

# def get_user(phone:str,db: Session):
#     user = db.query(User).filter(User.phone || User.email == phone).first()
#     return user
#UPDATED: user can login with phone or email
def get_user(phone: str, db: Session):
    user = db.query(User).filter(or_(User.phone == phone, User.email == phone)).first()
    return user


def get_user_by_email(email: User.email,  db:Session):             #new
    user = db.query(User).filter(User.email == email).first()
    return user

def sms_otp(phone: str, db: Session):
    try:
        #termil api integration
        user = db.query(User).filter(or_(User.phone == phone, User.email == phone)).first()

        if phone.startswith("0"):
            phone = "234" + phone[1:]
        url = "https://api.ng.termii.com/api/sms/otp/send"

        payload = {
            "api_key" : os.getenv("TERMII_API_KEY"),
            "message_type" : "NUMERIC",
            "to" : phone,
            "from" : "VTUking",
            "channel" : "generic",
            "pin_attempts" : 5,
            "pin_time_to_live" :  5,
            "pin_length" : 6,
            "pin_placeholder" : "< 1234 >",
            "message_text" : "Your pin is < 1234 >",
            "pin_type" : "NUMERIC"
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, json=payload)

        pin_d = response.text
        response_json = json.loads(pin_d)
        pin_id = response_json['pinId']
        user.sms_otp = pin_id
        db.commit() 
        print(response.text)
        print(pin_id)
    except Exception as e:
        print("An error occurred:", str(e))

    
   

def verify_sms_otp(phone: str, otp: str, db: Session):
    user = db.query(User).filter(User.phone == phone).first()

    
    url = "https://api.ng.termii.com/api/sms/otp/verify"

    payload = {
        "api_key": os.getenv("TERMII_API_KEY"),
          "pin_id": user.sms_otp,
          "pin": otp,
       }
    headers = {
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    #if response.status_code == 200: set phone_verified to true
    if response.status_code == 200:
        user.phone_verified = True
        db.commit()
        db.refresh(user)
        return user
    print(response.text)

#validate otp


