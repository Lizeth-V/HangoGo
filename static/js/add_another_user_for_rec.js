var usernames = [];
var locations = [];

document.addEventListener('DOMContentLoaded', function() {
    const addFriendBtn = document.getElementById('addFriendBtn');
    const friendForm = document.getElementById('friendForm');

    addFriendBtn.addEventListener('click', function() {
        // add username to the list of usernames
        var username = document.getElementById('userName');
        usernames.push(username.value);
        // add username to userAdded
        var userAdded = document.getElementById('userAdded');
        userAdded.innerHTML+=username.value+", ";
        //clear username
        username.value = '';

        //add location to the list of locations (if doesn't already exist)
        var location = document.getElementById('myInput');
        if (!locations.includes(location.value)){
            locations.push(location.value);
            //add location to the location output dropdown
            var locChoice = document.getElementById("locationOption");
            var addLoc = document.createElement("option");
            addLoc.value = location.value;
            addLoc.innerHTML = "Use " + location.value;
            locChoice.insertBefore(addLoc, locChoice.firstChild);
            locChoice.selectedIndex = 0;
        }
        //clear location
        location.value = '';
    });

    friendForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var locChoice = document.getElementById('locationOption').value;
        var coordinates = [];

        // pass in current user's location
        if (locChoice == "useYourLocation"){
            get_user_location(function(position) {
                var latitude = position.latitude;
                var longitude = position.longitude;
                coordinates.push([latitude, longitude])
        
                // get recommend with coordinates and usernames
                get_recommend(usernames, coordinates);
            })
        // pass in the other locations
        }else{
            if(locChoice == "useCenterLocation"){
                // pass in all locations
                for (const city of locations) {
                    coordinates.push(fetchCoordinates(city).Coordinates);
                }
            }else{
                // pass in coordinates of city
                coordinates.push(fetchCoordinates(locChoice).Coordinates);
            }
            // get recommend with coordinates and usernames
            get_recommend(usernames, coordinates);
        }

        // get recommend (based on Aidan's code)
        function get_recommend(usernames, locations){
            // refresh usernames and coordinates after submitting

            fetch('/get_multi_recommendation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ usernames: usernames, locations: locations }),
            })
            .then(response => response.json())
            .then(data => {
                var activePlace = data.active_place;
                var recName = document.getElementById('placeName');
                var recAddress = document.getElementById('placeAddress');
                var recLink = document.getElementById('placeLink');
                var recImage = document.getElementById('placeImage');
                
                recImage.src = activePlace.image_url;
                recImage.style.width = '300px';
                recImage.style.height = '200px';

                recName.innerHTML = activePlace.name;
                recAddress.innerHTML = activePlace.address;
                recLink.innerHTML = "View on web"
                recLink.href = activePlace.weblink;
            })
            .catch(error => {
                console.error('Error:', error);
            });

        }

        // fetchCoordinates from city
        function fetchCoordinates(city) {
            // Create a new XMLHttpRequest object
            var xhr = new XMLHttpRequest();
            var url = `/get_coordinates?city=${city}`;
            xhr.open('GET', url, false);
            xhr.send();
            if (xhr.status === 200) {
                return JSON.parse(xhr.responseText);
            } else {
                throw new Error('Failed to fetch data: ' + xhr.status);
            }
          }
    });

    // aidan's geolocation code
    function get_user_location(callback){
        //using the navigator interface we can get the gps location of the user using the browser.
        if (navigator.geolocation){
          navigator.geolocation.getCurrentPosition(
            function(position) {
                callback({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            });
        }
    }
});