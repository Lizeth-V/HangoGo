from flask import Flask, render_template, request
import generate_model
import temp_feedback
import return_highest_rec as retH


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_place_details')
def get_active_place_details(user_id=None):
    user_id = '6568cbef4a9658311b3ee704'  # Replace with actual user ID
    active_place = retH.match_highest_list(retH.get_highest_list(user_id), radius = 500, place_type = None)
    
    return render_template('index.html', active_place=active_place)


@app.route('/accept_rec/<user_id>/<place_id>', methods=['POST'])
def accept_rec_model(user_id=None, place_id=None):

    user_id = '6568cbef4a9658311b3ee704'  # Replace with actual user ID
    temp_feedback.accept_recommendation_update(user_id=user_id,place_id=place_id)
    generate_model.generate_place_probabilities(user_id)


    return render_template('result.html')  # You can customize this template as needed

@app.route('/decline_rec/<user_id>/<place_id>', methods=['POST'])
def decline_rec_model(user_id=None, place_id=None):
    
    user_id = '6568cbef4a9658311b3ee704'  # Replace with actual user ID
    temp_feedback.decline_recommendation_update(user_id=user_id, place_id=place_id)
    generate_model.generate_place_probabilities(user_id)


    return render_template('result.html')  # You can customize this template as needed'''

if __name__ == '__main__':
    app.run(debug=True)
