#db >repository > login.py
from sqlalchemy import or_
from sqlalchemy.orm import Session

from db.models.users import User 
import requests
import json

pin_id = {}

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
#termil api integration
    user = db.query(User).filter(or_(User.phone == phone, User.email == phone)).first()
    url = "https://api.ng.termii.com/api/sms/otp/send"
    payload = {
            "api_key" : "TLdt2cEASyCECDkbjpEewpl5VprA4VndOlJg3g2ujYfk9DSzM44GdLezLJWlwp",
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
    #pin_id = pin_d['pinId']
    response_json = json.loads(pin_d)
    pin_id = response_json['pinId']
    print(pin_id + user)
    
   

def verify_sms_otp(otp: str, db: Session):
    
    url = "https://api.ng.termii.com/api/sms/otp/verify"

    payload = {
        "api_key": "TLdt2cEASyCECDkbjpEewpl5VprA4VndOlJg3g2ujYfk9DSzM44GdLezLJWlwp",
          "pin_id": pin_id,
          "pin": otp,
       }
    headers = {
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.text)

#validate otp


