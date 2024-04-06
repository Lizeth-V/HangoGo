from flask import Flask, render_template, request, jsonify
import temp_feedback
import return_highest_rec as retH
import generate_model
from bson import ObjectId
import math
from celery import Celery
from get_history import pull_history


app = Flask(__name__)

@app.route('/')
def index():
    user_id = '6568cbef4a9658311b3ee704'  #test id until full implementation with the chat history box
    return render_template('history.html', user_id = user_id)

#convert to string
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None  
    else:
        return obj


@app.route('/inflate_user_history', methods=['GET'])
def fetch_user_history():

    user_id = '6568cbef4a9658311b3ee704'  #\test id

    user_rec_history = []
    #calculate the place and the feedback response and apply it to a list of strings to display.
    if user_id:
        for item in pull_history(user_id):
            if item['feedback'] == 0:
                fb = "rejected"
            else:
                fb = "accepted"
            user_rec_history.append('You ' + fb + ' a recommendation to ' + item['name'])
            
    return jsonify({'history': user_rec_history})


if __name__ == '__main__':
    app.run(debug=True)



    