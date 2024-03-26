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
    return render_template('chatbox.html', user_id = user_id)

#take in the parameters and return a recommendation, from the AI
@app.route('/get_new_active_place', methods=['GET'])
def get_active_place_details():
    user_id = '6568cbef4a9658311b3ee704'
    radius = request.args.get('radius', default=5, type=int)
    place_type = request.args.get('place_type', default=None, type=str)
    lat = request.args.get('lat', default=None, type=float)
    long = request.args.get('long', default=None, type=float)


    active_place = retH.match_highest_list(
        retH.get_highest_list(user_id),
        lat=lat,
        long=long,
        radius=radius,
        place_type=place_type
    )
    #Convert all ObjectId instances to strings for easier coding
    active_place = convert_objectid(active_place)

    #Return data to be displayed and used, as json.
    return jsonify({'active_place': active_place})

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

#Called when user presses accept
@app.route('/accept_rec/', methods=['GET'])
def accept_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user
    user_id = '6568cbef4a9658311b3ee704'  #temp
    place_id = request.args.get('place_id', default=None, type=str)


    if place_id:
        temp_feedback.accept_recommendation_update(user_id=user_id, place_id=place_id) #update the feedback page
        generate_model.generate_place_probabilities(user_id)

    return 'Success' 

#Called when user presses decline
@app.route('/decline_rec/', methods=['GET'])
def decline_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user
    user_id = '6568cbef4a9658311b3ee704'  #\test id
    place_id = request.args.get('place_id', default=None, type=str)


    temp_feedback.decline_recommendation_update(user_id=user_id, place_id=place_id)
    generate_model.generate_place_probabilities(str(user_id))

    return 'Success'


#Called when user presses block
@app.route('/block_rec/', methods=['GET'])
def block_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user, prevents this place from being shown again.
    user_id = '6568cbef4a9658311b3ee704'  #\test id
    place_id = request.args.get('place_id', default=None, type=str)


    temp_feedback.block_recommendation_update(user_id=user_id, place_id=place_id)
    generate_model.generate_place_probabilities(str(user_id))

    return 'Success'

#deprecated, we just save history as feedback instead, save data
@app.route('/save_chat/', methods=['GET'])
def save_messages():

    user_id = '6568cbef4a9658311b3ee704'  #\test id

    radius = request.args.get('radius', default=None, type=int)
    place_type = request.args.get('place_type', default=None, type=str)
    place_name = request.args.get('place_name', default=None, type=str)
    user_action = request.args.get('user_action', default=None, type=str)


    user_req_message = 'You' + ' asked for a recommendation'
    if place_type:
        user_req_message = user_req_message + ' of type ' + place_type
    if radius:
        user_req_message = user_req_message + ' in radius ' + radius
    user_req_message = user_req_message + '.'

    #temp_feedback.insert_user_chat(user_id=user_id, string=user_req_message)

    rec_message = 'Hango recommended ' + place_name + 'and you ' + user_action + 'ed it.'

    #temp_feedback.insert_user_chat(user_id=user_id, string=rec_message)

    return 'Success'


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



    