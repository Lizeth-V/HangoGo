import re
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session

from db import users_collection
from db import users_collection
from register import hash_password

app = Flask(__name__)

def reset_psw(username, newPassword ,users_collection):
    
    # Hash the new password
    hashed_password = hash_password(newPassword)

    print("Updates DB to have the new password")
    update_data = {

        "password": hashed_password
    }
    
    if update_data:
        users_collection.update_one(
            {'username': username},
            {'$set': update_data}
        )
        print("update user successful..?")
    else:
        print("no changes made")