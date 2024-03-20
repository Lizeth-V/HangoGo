

def landing_msg(user_name):
    #Hi name, yap yap yap, do you want to get started?

    #wait for input

def default_rec_msg(user_id):
    #rating number < 10: use Nhu Model
    #else: use Aidan Model
    #Produce recommendation
    #Add recommendation message card
    #Add recommendation card
    #wait for feedback

def filter_rec_msg(userid, radius, type):
    #rating number < 10: use Nhu Model
    #else: use Aidan Model
    #pass parameters
    #create a message card with parameters
    #add recommendation card
    #wait for feedback

def no_useable_rec_msg(user_id):
    #user num ratings >= num of places
    #no available recommendations
    #delete any recommendation feedback or oldest

def no_filtered_rec_msg(user_id,radius,type):
    #if place list return is empty, enter here
    #There are no recommendations within range and or type
    #Please expand your selections

def accepted_rec_msg(user_id,place_id):
    #cool let's hangogo to $place_name$
    
