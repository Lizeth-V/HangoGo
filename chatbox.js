document.getElementById('message-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var latitude;
    var longitude;

    get_user_location(function(position) {
        latitude = position.latitude;
        longitude = position.longitude;
        console.log("Latitude:", latitude);
        console.log("Longitude:", longitude);

        create_messages(latitude, longitude);
        // You can now use the latitude and longitude values here
    });
    
  }
);
  

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
    userImage.src = "{{ url_for('static', filename='hango.png') }}";
    userImage.className = 'user-image';

    user_req_message.appendChild(userImage);

////////////////////////////////////////////////////USER MESSAGE////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////HANGO MESSAGE////////////////////////////////////////////////////////////////

    var scrollDiv = document.querySelector('.scroll');
    scrollDiv.scrollTop = scrollDiv.scrollHeight;
    
    var messageContent = "Fun Choice! Here's what I came up with:";
    
    var newMessage = document.createElement('div');
    newMessage.className = 'message';

    var messageImage = document.createElement('img');
    messageImage.src = "{{ url_for('static', filename='hango.png') }}";
    messageImage.className = 'message-image';

    newMessage.appendChild(messageImage);
    newMessage.appendChild(document.createTextNode(messageContent));

    var messageStack = document.getElementById('message-stack');
////////////////////////////////////////////////////HANGO MESSAGE////////////////////////////////////////////////////////////////

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

    var rec_button_group = document.createElement('div');
    rec_button_group.className = 'rec-button-group';

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
          showQuery();
          scrollDiv.scrollTop = scrollDiv.scrollHeight;
        }, 5000); 

    };

    decline_button.onclick = function() {
        save_user_chat(user_id, radius, placeType, activePlace.name, 'decline');
        accept_button.remove();
        decline_button.remove();
        declineRec(place_id);
        setTimeout(() => {
          showQuery();
          scrollDiv.scrollTop = scrollDiv.scrollHeight;
        }, 5000); 
    };

    rec_button_group.appendChild(accept_button);
    rec_button_group.appendChild(decline_button);

    active_rec_message.appendChild(rec_info);
    active_rec_message.appendChild(rec_button_group);

    // Insert the active recommendation message into the message stack
    var messageStack = document.getElementById('message-stack');
    messageStack.insertBefore(user_req_message, messageStack.firstChild);
    scrollDiv.scrollTop = scrollDiv.scrollHeight;
    setTimeout(() => {
        messageStack.insertBefore(newMessage, messageStack.firstChild);
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }, 500); 
    setTimeout(() => {
        messageStack.insertBefore(active_rec_message, messageStack.firstChild);
        // Scroll to the bottom of the message stack
        var scrollDiv = document.querySelector('.scroll');
        hideQuery();
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
      }, 1000);

    
  })
  .catch(error => {
      // Handle any errors that occurred during the fetch
      console.error('Error:', error);
  });
}

  function showQuery(){
    var submit_elements = document.getElementById('message-form').elements;

    for (var i = 0; i < submit_elements.length; i++) {
      submit_elements[i].disabled = false;
      submit_elements[i].style.visibility = 'visible'; 
    }
    
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
              messageImage.src = "{{ url_for('static', filename='hango.png') }}";
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