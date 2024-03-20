from flask import Flask, render_template, request, jsonify
import temp_feedback
import return_highest_rec as retH
import generate_model
from bson import ObjectId
import math

app = Flask(__name__)

@app.route('/')
def index():
    user_id = '6568cbef4a9658311b3ee704'  #test id until full implementation with the chat history box
    return render_template('chatbox.html', user_id = user_id)

@app.route('/get_new_active_place', methods=['GET'])
def get_active_place_details():
    user_id = '6568cbef4a9658311b3ee704'
    radius = request.args.get('radius', default=5, type=int)
    place_type = request.args.get('place_type', default=None, type=str)
    
    active_place = retH.match_highest_list(
        retH.get_highest_list(user_id),
        radius=radius,
        place_type=place_type
    )
    # Convert all ObjectId instances to strings
    active_place = convert_objectid(active_place)

    return jsonify({'active_place': active_place})

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


@app.route('/accept_rec/<user_id>/<place_id>', methods=['POST'])
def accept_rec_model(user_id=None, place_id=None):

    user_id = '6568cbef4a9658311b3ee704'  #temp

    if place_id:
        p_id = str(place_id).lstrip("ObjectId('").rstrip("')") #strip the objectid from the string so its compatible with
        temp_feedback.accept_recommendation_update(user_id=user_id, place_id=p_id) #update the feedback page
        generate_model.generate_place_probabilities(user_id)

        return render_template('result.html')  #html for after

@app.route('/decline_rec/<user_id>/<place_id>', methods=['POST'])
def decline_rec_model(user_id=None, place_id=None):

    user_id = '6568cbef4a9658311b3ee704'  #\test id

    if place_id:
        p_id = str(place_id).lstrip("ObjectId('").rstrip("')")

        temp_feedback.decline_recommendation_update(user_id=user_id, place_id=p_id)
        generate_model.generate_place_probabilities(str(user_id))

    return render_template('result.html') 

@app.route('/block_rec/<user_id>/<place_id>', methods=['POST'])
def block_rec_model(user_id=None, place_id=None):

    user_id = '6568cbef4a9658311b3ee704'  #\test id

    if place_id:
        p_id = str(place_id).lstrip("ObjectId('").rstrip("')")

        temp_feedback.block_recommendation_update(user_id=user_id, place_id=p_id)
        generate_model.generate_place_probabilities(str(user_id))

    return render_template('result.html') 

if __name__ == '__main__':
    app.run(debug=True)



    