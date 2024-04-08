var latitude;
var longitude;
var data_lat;
var data_long;
var data_address;
var data_count;
var data;

// Geoloc not activated
var geo_loc = false;

hideQuery();

//other variables
var scrollDiv = document.querySelector('.scroll');
//message_info for user_location_prompt
var message_info = document.createElement('div');
message_info.className = 'message';
//loc button group
var loc_button_group = document.createElement('div');
loc_button_group.className = 'loc-button-group';
//rec button group
var rec_button_group = document.createElement('div');
rec_button_group.className = 'rec-button-group';


try {
  data = fetch_db_data('/get_db_data');
  data_lat = data.lat;
  data_long = data.long;
  data_address = data.address;
  data_count = data.db_count;
  } catch (error) {
    console.error(error);
  }

if (data_count<10){
  hideQuery();
}else{
  showQuery();
}

// get user location preference
user_location_prompt();

// run initial recommendations if less than 10 in database
loc_button_group.onclick = function() {
  //change prompt after location chosen
  message_info.childNodes[1].textContent= "Location chosen! Please select what recommendation you want in the form below and hit send!"
  if (data_count < 10){
    var messageContent;
    if (data_count == 0){
      messageContent = "Let's start rating so we can start recommending you! Please rate these 10 places:";
    }
    else{
      messageContent = "Continue rating so we can start recommending you! You have "+ (10-data_count)+ " places left to rate:";
    }
    var newMessage = document.createElement('div');
    newMessage.className = 'message';
    var messageImage = document.createElement('img');
    messageImage.src = "static/hango.png";
    messageImage.className = 'message-image';
    messageImage.style.visibility = 'hidden';
    newMessage.appendChild(messageImage);
    newMessage.appendChild(document.createTextNode(messageContent));
    //insert user_req_message into stack
    var messageStack = document.getElementById('message-stack');
    var radius = "None";
    var placeType = "None";
    hangogoRecommend(messageStack, newMessage, latitude, longitude, radius, placeType);
    data_count = fetch_db_data('/get_db_data').db_count;
    setTimeout(() => {
      messageStack.insertBefore(newMessage, messageStack.firstChild);
      scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }, 500); 
    rec_button_group.onclick = function(){
      hangogoRecommend(messageStack, newMessage, latitude, longitude, radius, placeType);
      data_count = fetch_db_data('/get_db_data').db_count;
      if (data_count>=10){
        newMessage.childNodes[1].textContent = "You finished rating 10 places! Please select what recommendation you want in the form below and hit send!";
        setTimeout(() => {
          messageStack.insertBefore(newMessage, messageStack.firstChild);
          scrollDiv.scrollTop = scrollDiv.scrollHeight;
        }, 500); 
        showQuery();
      }
    }
  }
};



// run recommendations based on user preference
document.getElementById('message-form').addEventListener('submit', function(e) {
  e.preventDefault();
  if (geo_loc){
    get_user_location(function(position) {
      latitude = position.latitude;
      longitude = position.longitude;
      create_messages(latitude, longitude);
    });
  }else{
    create_messages(latitude, longitude);
  }
});

function user_location_prompt(){
  var new_message = document.createElement('div');
  new_message.className = 'active-rec-message';

  let mes_content = "Please choose which location you want to use to start recommending for!";

  var message_image = document.createElement('img');
  message_image.src = "static/hango.png";
  message_image.className = 'message-image';

  message_info.appendChild(message_image);
  message_info.appendChild(document.createTextNode(mes_content));

  // turn on location services button
  var geoloc_button = document.createElement('button');
  geoloc_button.className = 'loc-button';
  geoloc_button.textContent = 'Use your current location';

  //database button
  var database_button = document.createElement('button');
  database_button.className = 'loc-button';
  database_button.textContent = data_address;

  //new loc button
  var new_loc_button = document.createElement('button');
  new_loc_button.className = 'loc-button';
  new_loc_button.textContent = 'Use a new location';

  //geoloc button functionality
  geoloc_button.onclick = function() {
    //hide other buttons, call the get_user_loc function
    geoloc_button.remove();
    database_button.remove();
    new_loc_button.remove();
    geo_loc = true;
    setTimeout(() => {
      scrollDiv.scrollTop = scrollDiv.scrollHeight;
      }, 5000); 
  };

  //database button functionality
  database_button.onclick = function() {
    //hide other buttons, call the decline function, after some time reveal search bar again
    geoloc_button.remove();
    database_button.remove();
    new_loc_button.remove();
    latitude = data_lat;
    longitude = data_long;
    setTimeout(() => {
      scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }, 5000); 
  };
  //new loc button functionality
  new_loc_button.onclick = function() {
    //hide other buttons, call the decline function, after some time reveal search bar again
    geoloc_button.remove();
    database_button.remove();
    new_loc_button.remove();
    setTimeout(() => {
      scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }, 5000); 
  };

  loc_button_group.appendChild(geoloc_button);
  loc_button_group.appendChild(database_button);
  loc_button_group.appendChild(new_loc_button);

  new_message.appendChild(message_info);
  new_message.appendChild(loc_button_group);

  var message_stack = document.getElementById('message-stack');
  message_stack.appendChild(new_message);
  //message_stack.insertBefore(new_message, message_stack.firstChild);
}

function fetch_db_data(url) {
  // Create a new XMLHttpRequest object
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, false);
  xhr.send();
  if (xhr.status === 200) {
      return JSON.parse(xhr.responseText);
  } else {
      throw new Error('Failed to fetch data: ' + xhr.status);
  }
}

function hideQuery(){
  var submit_elements = document.getElementById('message-form').elements;

  for (var i = 0; i < submit_elements.length; i++) {
    submit_elements[i].disabled = true;
    submit_elements[i].style.visibility = 'hidden'; 
  }
  
  var add_elements = document.getElementById('additional-fields');
  
  add_elements.innerHTML = '';

  var selector = document.getElementById('message_type');
  if (selector) {
      selector.selectedIndex = 0;
  }
}


function showQuery(){
  var submit_elements = document.getElementById('message-form').elements;

  for (var i = 0; i < submit_elements.length; i++) {
    submit_elements[i].disabled = false;
    submit_elements[i].style.visibility = 'visible'; 
  }
  
}

function create_messages(latitude,longitude) {
  var messageType = document.getElementById('message_type').value;
  var radius = document.getElementById('radius') ? document.getElementById('radius').value : '';
  var placeType = document.getElementById('place_type') ? document.getElementById('place_type').value : '';

  var messageContent = "";

  if (messageType == "default") {
    messageContent = "Take me Anywhere!";
  }
  else if (messageType == "radius") {
    messageContent = "Take me somewhere in ";
    messageContent += radius;
    messageContent += " miles";
  }
  else if (messageType == "type") {
    messageContent = "Take me somewhere that invloves ";
    messageContent += placeType;
  }
  else if (messageType == "type_radius") {
    messageContent = "Take me somewhere in ";
    messageContent += radius;
    messageContent += " miles";
    messageContent += " that invloves ";
    messageContent += placeType
  }

  var user_req_message = document.createElement('div');
  user_req_message.className = 'user-message';

  user_req_message.appendChild(document.createTextNode(messageContent));

  var userImage = document.createElement('img');
  userImage.src = "/static/hango.png";
  userImage.className = 'user-image';

  user_req_message.appendChild(userImage);

////////////////////////////////////////////////////USER MESSAGE////////////////////////////////////////////////////////////////
  hangogoResponse(user_req_message, latitude, longitude, radius, placeType);
}

function hangogoResponse(user_req_message, latitude, longitude, radius, placeType){
  ////////////////////////////////////////////////////HANGO MESSAGE////////////////////////////////////////////////////////////////
  scrollDiv.scrollTop = scrollDiv.scrollHeight;

  var messageContent = "Fun Choice! Here's what I came up with:";

  var newMessage = document.createElement('div');
  newMessage.className = 'message';

  var messageImage = document.createElement('img');
  messageImage.src = "static/hango.png";
  messageImage.className = 'message-image';

  newMessage.appendChild(messageImage);
  newMessage.appendChild(document.createTextNode(messageContent));

  //insert user_req_message into stack
  var messageStack = document.getElementById('message-stack');
  messageStack.insertBefore(user_req_message, messageStack.firstChild);
  scrollDiv.scrollTop = scrollDiv.scrollHeight;
  setTimeout(() => {
    messageStack.insertBefore(newMessage, messageStack.firstChild);
    scrollDiv.scrollTop = scrollDiv.scrollHeight;
}, 500); 

  hangogoRecommend(messageStack, newMessage, latitude, longitude, radius, placeType);
  ////////////////////////////////////////////////////HANGO MESSAGE////////////////////////////////////////////////////////////////
}

function hangogoRecommend(messageStack, newMessage, latitude, longitude, radius, placeType){
  ////////////////////////////////////////////////////REC MESSAGE////////////////////////////////////////////////////////////////
  var user_id = ""
  fetchActivePlaceAndUpdate(user_id, latitude, longitude, radius, placeType)
  .then(activePlace => {
    var place_id = activePlace._id
    // Create the active recommendation message elements
    var active_rec_message = document.createElement('div');
    active_rec_message.className = 'active-rec-message';

    var rec_info = document.createElement('div');
    rec_info.className = 'rec-info';

    var rec_image = document.createElement('img');
    rec_image.src = activePlace.image_url;
    rec_image.className = 'rec-image';

    var rec_text_info = document.createElement('div');
    rec_text_info.className = 'rec-text-info';

    var rec_title = document.createElement('h1');
    rec_title.textContent = activePlace.name;

    var rec_address = document.createElement('h2');
    rec_address.textContent = activePlace.address;

    rec_text_info.appendChild(rec_title);
    rec_text_info.appendChild(rec_address);

    rec_info.appendChild(rec_image);
    rec_info.appendChild(rec_text_info);

    var accept_button = document.createElement('button');
    accept_button.className = 'accept-button';
    accept_button.textContent = 'Accept';

    var decline_button = document.createElement('button');
    decline_button.className = 'decline-button';
    decline_button.textContent = 'Decline';

    accept_button.onclick = function() {
        save_user_chat(user_id, radius, placeType, activePlace.name, 'accept');
        accept_button.remove();
        decline_button.remove();
        acceptRec(place_id);
        setTimeout(() => {
          scrollDiv.scrollTop = scrollDiv.scrollHeight;
        }, 5000); 

    };

    decline_button.onclick = function() {
        save_user_chat(user_id, radius, placeType, activePlace.name, 'decline');
        accept_button.remove();
        decline_button.remove();
        declineRec(place_id);
        setTimeout(() => {
          scrollDiv.scrollTop = scrollDiv.scrollHeight;
        }, 5000); 
    };

    rec_button_group.appendChild(accept_button);
    rec_button_group.appendChild(decline_button);

    active_rec_message.appendChild(rec_info);
    active_rec_message.appendChild(rec_button_group);

    // insert the active recommendation message into the message stack
    setTimeout(() => {
        messageStack.insertBefore(active_rec_message, messageStack.firstChild);
        // Scroll to the bottom of the message stack
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
      }, 1000);
    })
  .catch(error => {
      // Handle any errors that occurred during the fetch
      console.error('Error:', error);
  });
}

function fetchActivePlaceAndUpdate(user_id, lat, long,radius, placeType) {
    var url = `/get_new_active_place?user_id=${user_id}&lat=${lat}&long=${long}&radius=${radius}&place_type=${placeType}`;
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            return data.active_place;
        })
        .catch(error => {
            console.error('Error:', error);
            throw error;
        });
}

function acceptRec(place_id) {
  var url = `/accept_rec?place_id=${place_id}`;
  return fetch(url)
  .catch(error => {
            console.error('Error:', error);
            throw error;
  });
  //Here is where we would set active place to focus
}

function declineRec(place_id) {
  var url = `/decline_rec?place_id=${place_id}`;
  return fetch(url)
  .catch(error => {
            console.error('Error:', error);
            throw error;
  });
  //Here is where we would set active place to focus
}

function blockRec(place_id) {
  var url = `/block_rec?place_id=${place_id}`;
  return fetch(url)
  .catch(error => {
            console.error('Error:', error);
            throw error;
  });
}

function get_user_location(callback){
  if (navigator.geolocation){
    navigator.geolocation.getCurrentPosition(
      function(position) {
          callback({
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
          });
      }
        , catch_loc_error);
  }
  //else not supported by browser idk the solution to this
}


function save_user_chat(user_id, radius, place_type, place_name, user_action) {
    var url = `/save_chat?user_id=${user_id}&radius=${radius}&place_type=${place_type}&place_name=${place_name}&user_action=${user_action}`;
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            return data.active_place;
        })
        .catch(error => {
            console.error('Error:', error);
            throw error;
        });
}


function catch_loc_error(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.log("User denied the request for Geolocation.");
            var messageContent = "Sorry, but without a location, I can't recommend :(, please activate your location services and try again!";
  
            var newMessage = document.createElement('div');
            newMessage.className = 'message';

            var messageImage = document.createElement('img');
            messageImage.src = "static/hango.png";
            messageImage.className = 'message-image';

            newMessage.appendChild(messageImage);
            newMessage.appendChild(document.createTextNode(messageContent));

            var messageStack = document.getElementById('message-stack');
            messageStack.insertBefore(newMessage, messageStack.firstChild);
            break;
        case error.POSITION_UNAVAILABLE:
            console.log("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            console.log("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            console.log("An unknown error occurred.");
            break;
    }
}



function showFields() {
  var selection = document.getElementById("message_type").value;
  var fieldsContainer = document.getElementById("additional-fields");
  fieldsContainer.innerHTML = ""; // Clear the previous fields

  if (selection === "radius" || selection === "type_radius") {
    // If radius is needed, add the radius input field
    fieldsContainer.innerHTML += `
      <label for="radius">Radius (in miles):</label>
      <select id="radius" name="radius" required>
        <option value="">Please select...</option>
        <option value="5">5 mi</option>
        <option value="10">10 mi</option>
        <option value="20">20 mi</option>
      </select><br>
    `;
  }

  if (selection === "type" || selection === "type_radius") {
    // If type is needed, add the place type dropdown
    fieldsContainer.innerHTML += `
      <label for="place_type">Place Type:</label>
      <select id="place_type" name="place_type" required>
        <option value="">Please select...</option>
        <option value="Food">Food</option>
        <option value="Drinks">Drinks</option>
        <option value="Entertainment">Entertainment</option>
        <option value="Nature/Recreation">Nature/Recreation</option>
        <option value="Museum/Art">Museum/Art</option>
        <option value="Nightlife">Nightlife</option>
      </select><br>
    `;
  }
}