function setActivePlace(user_id, place_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/set_active_place_route', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response);
        }
    };
    var data = JSON.stringify({user_id: user_id, place_id: place_id});
    xhr.send(data);
}

// function setActivePlaceAndChangeToMap(user_id, place_id) {
//     setActivePlace(user_id, place_id);
//     // call change to map here
//     // changeToMap(user_id);
// }