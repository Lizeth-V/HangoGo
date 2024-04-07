from flask import Flask, render_template, request, jsonify
import temp_feedback
import return_highest_rec as retH
import generate_model
from bson import ObjectId
import math
from celery import Celery
import get_history

app = Flask(__name__)

#I worked on my section of the app.py in my own file, it however is now fully implemented into the app.py file

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("chatbox.html")

#(Aidan)
#take in the parameters and return a recommendation, from the AI
@app.route('/get_new_active_place', methods=['GET', 'POST'])
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

#(Aidan)
#convert to string for handling bson objects
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

#(Aidan)
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

#(Aidan)
#Called when user presses decline
@app.route('/decline_rec/', methods=['GET'])
def decline_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user
    user_id = '6568cbef4a9658311b3ee704'  #\test id
    place_id = request.args.get('place_id', default=None, type=str)


    temp_feedback.decline_recommendation_update(user_id=user_id, place_id=place_id)
    generate_model.generate_place_probabilities(str(user_id))

    return 'Success'


#(Aidan)
#Called when user presses block
@app.route('/block_rec/', methods=['GET'])
def block_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user, prevents this place from being shown again.
    user_id = '6568cbef4a9658311b3ee704'  #\test id
    place_id = request.args.get('place_id', default=None, type=str)

    temp_feedback.block_recommendation_update(user_id=user_id, place_id=place_id)
    generate_model.generate_place_probabilities(str(user_id))

    return 'Success'

#(Aidan)
@app.route('/save_chat/', methods=['GET'])
def save_messages():
    #accept user id in the url and replace
    user_id = '6568cbef4a9658311b3ee704'  #\test id

    #accept arguments from url
    radius = request.args.get('radius', default=None, type=int)
    place_type = request.args.get('place_type', default=None, type=str)
    place_name = request.args.get('place_name', default=None, type=str)
    user_action = request.args.get('user_action', default=None, type=str)


    #structure of the chat history storage
    user_req_message = 'You' + ' asked for a recommendation'
    if place_type:
        user_req_message = user_req_message + ' involving ' + place_type
    if radius:
        user_req_message = user_req_message + ' in a radius of ' + str(radius) +' miles'
    user_req_message = user_req_message + '.'

    temp_feedback.insert_user_chat(user_id=user_id, string=user_req_message, source='hango')

    #also store the user feedback
    if user_action == 'decline':
        rec_message = 'Hango recommended ' + place_name + ' and you ' + user_action + 'd it.'
    else:
        rec_message = 'Hango recommended ' + place_name + ' and you ' + user_action + 'ed it.'

    #save to database
    temp_feedback.insert_user_chat(user_id=user_id, string=rec_message, source='user')

    return 'Success'

#(Aidan)
#when called, it brings in the user chat history and inflates their history page with it
@app.route('/inflate_user_history', methods=['GET'])
def fetch_user_history():

    user_id = '6568cbef4a9658311b3ee704'  #\test id

    user_rec_history = get_history.get_user_history(user_id)
    
    #return the chat history as a json to be able to print
    return jsonify({'history': user_rec_history})

#(Aidan)
#flask call to delete user histories
@app.route('/delete_user_chats', methods=['GET'])
def delete_user_history():

    user_id = '6568cbef4a9658311b3ee704'  #\test id

    temp_feedback.delete_user_chat_history(user_id)
    
    return 'Success'


if __name__ == '__main__':
    app.run(debug=True)



    
    