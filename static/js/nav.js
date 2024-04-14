function fetch_active_place(user_id) {
    var url = `/fetch_user_active_place?user_id=${user_id}`;

    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}


function changeToMap(user_id, place_name, place_address, place_coordinates, user_coordinates) {
    if (place_name == undefined){
        var user_id = document.getElementById("userID").innerHTML

        get_user_location(function(position) {
            latitude = position.latitude;
            longitude = position.longitude;

            fetch_active_place(user_id)
            .then(data => { 
                if (data.name != undefined){
                        place_name = data.name;

                        user_coordinates = latitude + "," + longitude;
                        place_coordinates = data.lat + "," + data.lon;
                        place_address = data.address;

                            var distance = calculateDistance(user_coordinates, place_coordinates);

                            var newhtml = '<div class="map">' +
                            '<iframe width="90%" height="50%" frameborder="0" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps/embed/v1/directions?key=AIzaSyDC1Ysg0I0IHqCs_TDxFwkMJDK71zruEGk' +
                            '&origin=' + encodeURIComponent(user_coordinates) +
                            '&destination=' + encodeURIComponent(place_address) +
                            '&avoid=tolls|highways" allowfullscreen></iframe>' +
                            '<h1>' + place_name + '</h1>' +
                            '<p>' + place_address + '</p>' +
                            '<p>Distance: ' + distance + ' km</p>' +
                            '<div class="map-buttons">'+
                            '<div class="favorite-map-button"><img src="static/star-regular-48.png"/><h1>favorite</h1></div>'+
                            '<div class="remove-map-button"><img src="static/x-circle-solid-48.png"/><h1>remove</h1></div>'+
                            '</div>'+
                            '<img class="report-map-button" src="staticerror-circle-regular-24.png"/>';

                            savedhtml = document.getElementById('userProfileContainer').innerHTML;
                            document.getElementById('userProfileContainer').innerHTML = newhtml;
                    
                            document.getElementById('map_button').innerHTML = '<a><i class="bx bxs-map-pin icon"></i></a>';
                            document.getElementById('user_p_button').innerHTML = '<a onclick="changeToProfile()"><i class="bx bxs-user-detail icon"></i></a>';
                    
                        }
                else{
                        var newhtml = 
                        '<div class="map">' +
                            '<iframe ' +
                                'width="90%" ' +
                                'height="50%" ' +
                                'frameborder="0" ' +
                                'style="border:0" ' +
                                'referrerpolicy="no-referrer-when-downgrade" ' +
                                'src="https://www.google.com/maps/embed/v1/place?key=AIzaSyDC1Ysg0I0IHqCs_TDxFwkMJDK71zruEGk&q=' + encodeURIComponent(latitude + "," + longitude) + '" ' +
                                    'allowfullscreen>' +
                            '</iframe>' +
                            '<h1>No Active Place</h1>' +
                        '</div>';

                        savedhtml = document.getElementById('userProfileContainer').innerHTML;
                        document.getElementById('userProfileContainer').innerHTML = newhtml;
                
                        document.getElementById('map_button').innerHTML = '<a><i class="bx bxs-map-pin icon"></i></a>';
                        document.getElementById('user_p_button').innerHTML = '<a onclick="changeToProfile()"><i class="bx bxs-user-detail icon"></i></a>';
                
                    }
                }
                )
            .catch(error => {
                // Handle any errors that occurred during fetch_active_place
                console.error("Error fetching active place:", error);
            });

         });
    }

    else{
        var distance = calculateDistance(user_coordinates, place_coordinates);

        var newhtml = '<div class="map">' +
        '<iframe width="90%" height="50%" frameborder="0" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps/embed/v1/directions?key=AIzaSyDC1Ysg0I0IHqCs_TDxFwkMJDK71zruEGk' +
        '&origin=' + encodeURIComponent(user_coordinates) +
        '&destination=' + encodeURIComponent(place_address) +
        '&avoid=tolls|highways" allowfullscreen></iframe>' +
        '<h1>' + place_name + '</h1>' +
        '<p>' + place_address + '</p>' +
        '<p>Distance: ' + distance + ' km</p>' +
        '<div class="map-buttons">'+
        '<div class="favorite-map-button"><img src="static/star-regular-48.png"/><h1>favorite</h1></div>'+
        '<div class="remove-map-button"><img src="static/x-circle-solid-48.png"/><h1>remove</h1></div>'+
        '</div>'+
        '<img class="report-map-button"/>';

        savedhtml = document.getElementById('userProfileContainer').innerHTML;
        document.getElementById('userProfileContainer').innerHTML = newhtml;
    
        document.getElementById('map_button').innerHTML = '<a><i class="bx bxs-map-pin icon"></i></a>';
        document.getElementById('user_p_button').innerHTML = '<a onclick="changeToProfile()"><i class="bx bxs-user-detail icon"></i></a>';    
    }

}

//haversine formula, find distance over sphere (Earth)
function calculateDistance(coords1, coords2) {
    var [lat1, lon1] = coords1.split(',').map(Number);
    var [lat2, lon2] = coords2.split(',').map(Number);

    var R = 6371; // Radius of the Earth in km
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLon = (lon2 - lon1) * Math.PI / 180;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var distance = R * c;

    return distance.toFixed(2);
}


function changeToProfile() {
    var user_id = document.getElementById("userID").innerHTML

    document.getElementById('map_button').innerHTML = `<a onclick="changeToMap('${user_id}')"><i class="bx bxs-map-pin icon"></i></a>`;
    document.getElementById('user_p_button').innerHTML = '<a><i class="bx bxs-user-detail icon"></i></a>';

    document.getElementById('userProfileContainer').innerHTML = savedhtml;

}