from pymongo import MongoClient, ReadPreference
import random
import string
from misc import random_id

cluster = MongoClient("mongodb+srv://main_user:mongo_password@cluster0.lse7t.mongodb.net/", read_preference=ReadPreference.PRIMARY, connectTimeoutMS=5000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
login_db = cluster.project_1.login_db
invite_code_db = cluster.project_1.invite_code_db
password_reset_db = cluster.project_1.pass_recover_db


def check_email(email):
    user_email = login_db.find_one({"email": email})
    if user_email != None:
        return True
    else:
        return False     

def check_login(email, password):
    user_email = login_db.find_one({"email": email})
    if user_email != None:
        if user_email["password"] == password:
            return user_email
        else:
            return False
    else:
        return False  

def check_invite(invite_code):
    invite_code_set = invite_code_db.find_one({"_id": invite_code})
    if invite_code_set != None:
        uses = int(invite_code_set["uses"])
        if uses >= 1:
            if uses - 1 == 0:
                invite_code_db.delete_one({"_id": invite_code})
                print(f"{invite_code} Removed")
                return True
            else:    
                invite_code_db.update_one({"_id": invite_code}, {"$set": {"uses": uses - 1}})
                return True
        else:
            invite_code_db.remove({"_id": invite_code})        
            return False
    else:
        return False

def change_pass(password, new_password):
    login_db.update_one({"password": password}, {"$set": {"password": new_password}})
    return True

def add_user(email, password, license):
    login_db.insert_one({"_id": random_id(), "email": email, "password": password, "license": license, "license_type": "Beta User", "plan_type": "£0/m", "hwid": "N/A"})
    return True

def add_pass_token(token, email):
    password_reset_db.insert_one({"_id": token, "email": email})
    return True

def fetch_pass_token(token, email):
    user_token = password_reset_db.find_one({"_id": token})
    if user_token != None:
        user_email = user_token["email"]

        if user_email == email:
            return True
        else:
            return False
    else:
        return False   

def delete_pass_token(token):
    password_reset_db.delete_one({"_id": token})
    return True 

def password_reset(email, new_password):
    login_db.update_one({"email": email}, {"$set": {"password": new_password}})
    return True

def fetch_user(license):
    user = login_db.find_one({"license": license})    
    if user != None:
        return user

    return False    

def set_hwid(license, hwid):
    login_db.update_one({"license": license}, {"$set": {"hwid": hwid}}) 

def reset_hwid(email, password):
    user = login_db.find_one({"email": email})
    if user != None:
        if user["password"] == password:
            login_db.update_one({"email": email}, {"$set": {"hwid": "N/A"}})
        else:
            return False
    else:
        return False