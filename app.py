from flask import Flask, render_template, request
import temp_feedback
import return_highest_rec as retH
import generate_model

app = Flask(__name__)

@app.route('/')
def index():
    user_id = '6568cbef4a9658311b3ee704'  #test id until full implementation with the chat history box
    active_place = retH.match_highest_list(retH.get_highest_list(user_id), radius = 20, place_type = None)
    
    return render_template('card.html', active_place=active_place, user_id = user_id)

@app.route('/get_place_details')
def get_active_place_details(user_id=None):
    user_id = '6568cbef4a9658311b3ee704'  
    active_place = retH.match_highest_list(retH.get_highest_list(user_id), radius = 20, place_type = None)
    
    return render_template('card.html', active_place=active_place, user_id = user_id)


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



    