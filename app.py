from flask import Flask, render_template, request
import generate_model
import temp_feedback


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

'''@app.route('/accept_rec', methods=['POST'])
def accept_rec_model(user_id=, place_id=):

    user_id = '6568cbef4a9658311b3ee704'  # Replace with actual user ID
    temp_feedback.accept_recommendation_update(user_id=user_id,place_id=place_id)
    generate_model.generate_place_probabilities(user_id)


    return render_template('result.html')  # You can customize this template as needed

@app.route('/decline_rec', methods=['POST'])
def decline_rec_model(user_id=, place_id=):
    
    user_id = '6568cbef4a9658311b3ee704'  # Replace with actual user ID
    temp_feedback.decline_recommendation_update(user_id=user_id, place_id=place_id)
    generate_model.generate_place_probabilities(user_id)


    return render_template('result.html')  # You can customize this template as needed'''

if __name__ == '__main__':
    app.run(debug=True)
