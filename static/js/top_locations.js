// Uses user location to calculate the top places around them 
// sending the location info back to flask app.py to update the query..
function sendLocationToFlask(latitude, longitude) {
    var data = {
        "latitude": latitude,
        "longitude": longitude
    };

    $.ajax({
        type: "POST",
        url: "/top_locations",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function() {
            console.log("Location sent to Flask successfully.");
        },
        error: function(error) {
            console.error("Error sending location to Flask:", error);
        }
    });
}
// Influenced by Nhu's code :)
function get_user_location(callback){
    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(
            function(position) {
                callback({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
                
            },
            function(error) {
                console.error('Error getting user location:', error);
            }
        );
    } else {
        // Geolocation not supported by browser
        console.error('Geolocation is not supported by this browser.');
    }
}

function reloadPage(){
    window.location.reload(true)
}


get_user_location(function(position) {
    var latitude = position.latitude;
    var longitude = position.longitude;
    console.log("Latitude:", latitude);
    console.log("Longitude:", longitude);
    sendLocationToFlask(latitude, longitude);
});


