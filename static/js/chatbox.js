document.getElementById('message-form').addEventListener('submit', function(e) {
  //This is the function that will run when the sumbit button is clicked
    e.preventDefault();
    var latitude;
    var longitude; 
    //Get the latitude and longitude using geolocator
    get_user_location(function(position) {
        latitude = position.latitude;
        longitude = position.longitude;
        //console.log("Latitude:", latitude);
        //console.log("Longitude:", longitude);

        //call the system to fetch place and create messages
        create_messages(latitude, longitude);
    });
    
  }
);
  
  //this simply hides the submit elements
  function hideQuery(){
    document.getElementById('submit_button').style.display = 'none';

    var submit_elements = document.getElementById('message-form').elements;

    for (var i = 0; i < submit_elements.length; i++) {
      submit_elements[i].disabled = true;
      submit_elements[i].style.visibility = 'hidden'; 
    }

    //hide every element in the class
    
    var add_elements = document.getElementById('additional-fields');
    
    add_elements.innerHTML = '';
    //resetting the html everytime for the additional fields 

    //set the selection to the default, so that the additional fields doesn't break
    var selector = document.getElementById('message_type');
    if (selector) {
        selector.selectedIndex = 0;
    }
  }


  //creates all three messages. These combined can be viewed as a single message in the scope of the system. Only the place recommendation is the variance and importance.
  function create_messages(latitude,longitude) {
    var messageType = document.getElementById('message_type').value;
    var radius = document.getElementById('radius') ? document.getElementById('radius').value : '';
    var place_type = document.getElementById('place_type') ? document.getElementById('place_type').value : '';
    var scroll_div = document.querySelector('.scroll');
    //get additional fields values

    var mes_content = "";

    //no functionality other than for visual
    //if default use default, else if type or radius or type radius.
    if (messageType == "default") {
      mes_content = "Take me Anywhere!";
    }
    else if (messageType == "radius") {
      mes_content = "Take me somewhere in ";
      mes_content += radius;
      mes_content += " miles";
    }
    else if (messageType == "type") {
      mes_content = "Take me somewhere that involves ";
      mes_content += place_type;
    }
    else if (messageType == "type_radius") {
      mes_content = "Take me somewhere in ";
      mes_content += radius;
      mes_content += " miles";
      mes_content += " that involves ";
      mes_content += place_type
    }

    //create the user message container
    var user_req_message = document.createElement('div');
    user_req_message.className = 'user-message';

    //appply text
    user_req_message.appendChild(document.createTextNode(mes_content));

    //add the user image
    var userImage = document.createElement('img');
    userImage.src = "/static/user-solid-24.png";
    //replace this with the user's uploaded image
    userImage.className = 'user-image';

    user_req_message.appendChild(userImage);

////////////////////////////////////////////////////USER MESSAGE////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////HANGO MESSAGE////////////////////////////////////////////////////////////////
    
    //AI's response message
    //Set as a singular default for now.
    var mes_content = "Fun Choice! Here's what I came up with:";
    
    //create container
    var new_message = document.createElement('div');
    new_message.className = 'message';

    //add hango image from static
    var message_image = document.createElement('img');
    message_image.src = "/static/hango.png";
    message_image.className = 'message-image';

    //append in the order so hango is on left and message on right
    new_message.appendChild(message_image);
    new_message.appendChild(document.createTextNode(mes_content));

////////////////////////////////////////////////////HANGO MESSAGE////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////REC MESSAGE////////////////////////////////////////////////////////////////
  var user_id = ""
  //replace user_id with the user_data code
  fetch_and_update_active_place(user_id, latitude, longitude, radius, place_type)
  //if the fetch works on the user in the current spot
  .then(activePlace => {
    //set active id
    //this might be unnecessary actually
    var place_id = activePlace._id

    //create a new container for the recommendation to display in the message, looks the same as hango's
    var active_rec_message = document.createElement('div');
    active_rec_message.className = 'active-rec-message';

    //this includes image and text descriptions
    var rec_info = document.createElement('div');
    rec_info.className = 'rec-info';

    //set active place image to the one fetched
    var img_container = document.createElement('div');
    img_container.className = 'rec-image';
    img_container.style.backgroundImage = 'url("' + activePlace.image_url + '")';

    //this is just for visual
    img_container.style.backgroundSize = 'cover';
    img_container.style.backgroundPosition = 'center'; 
    img_container.style.backgroundRepeat = 'no-repeat';
    
    //this isn't actually used I was debugging something and settled with switching the backgroun of the parent container, leave for now
    var rec_image = document.createElement('img');
    rec_image.src = activePlace.image_url;
    rec_image.className = 'r-image';
    
    img_container.appendChild(rec_image)

    //text container for the reccomendation
    var rec_text_info = document.createElement('div');
    rec_text_info.className = 'rec-text-info';

    //Name
    var rec_title = document.createElement('h1');
    rec_title.textContent = activePlace.name;

    //Address
    var rec_address = document.createElement('h2');
    rec_address.textContent = activePlace.address;

    //Be able to view it on the web
    var web_link = document.createElement('a');
    web_link.textContent = "View on web";
    web_link.href = activePlace.weblink;
    web_link.target = "_blank"

    //add to the text container
    rec_text_info.appendChild(rec_title);
    rec_text_info.appendChild(rec_address);
    rec_text_info.appendChild(web_link);

    //add to the flexbox container
    rec_info.appendChild(img_container);
    rec_info.appendChild(rec_text_info);

    //create button group
    var rec_button_group = document.createElement('div');
    rec_button_group.className = 'rec-button-group';

    //accept rec button
    var accept_button = document.createElement('button');
    accept_button.className = 'accept-button';
    accept_button.textContent = 'Accept';

    //decline rec button
    var decline_button = document.createElement('button');
    decline_button.className = 'decline-button';
    decline_button.textContent = 'Decline';

    //container for the block and the report buttons
    var util_button_group = document.createElement('div');
    util_button_group.className = 'util-button-group';

    //block "button", clickable image
    var block_button = document.createElement('img');
    block_button.className = 'block-button';
    block_button.src = "static/block-regular-24.png";  
    block_button.alt = "Block Place";
    block_button.title = "Block Place";

    //report "button", clickable image
    var report_button = document.createElement('img');
    report_button.className = 'block-button';
    report_button.src = "static/error-circle-regular-24.png";
    block_button.alt = "Report Place";
    report_button.title = "Report Place";
    

    //accept button functionality
    accept_button.onclick = function() {
      //hide other buttons, call the accept function, after some time reveal search bar again
        save_user_chat(user_id, radius, place_type, activePlace.name, 'accept');
        accept_button.remove();
        decline_button.remove();
        block_button.remove();
        report_button.remove();
        accept_rec(place_id);
        setTimeout(() => {
          show_query();
          scroll_div.scrollTop = scroll_div.scrollHeight;
        }, 5000); 

    };

    decline_button.onclick = function() {
      //hide other buttons, call the decline function, after some time reveal search bar again
        save_user_chat(user_id, radius, place_type, activePlace.name, 'decline');
        accept_button.remove();
        decline_button.remove();
        block_button.remove();
        report_button.remove();
        decline_rec(place_id);
        setTimeout(() => {
          show_query();
          scroll_div.scrollTop = scroll_div.scrollHeight;
        }, 5000); 
    };

    block_button.onclick = function() {
      //hide other buttons, call the block function, after some time reveal search bar again
      save_user_chat(user_id, radius, place_type, activePlace.name, 'blocked');
      accept_button.remove();
      decline_button.remove();
      block_button.remove();
      report_button.remove();
      block_rec(place_id);
      setTimeout(() => {
        show_query();
        scroll_div.scrollTop = scroll_div.scrollHeight;
      }, 5000); 
  };

  //add report functionality, since it is a different process
  report_button.onclick = function() {
        //save_user_chat(user_id, radius, place_type, activePlace.name, 'decline');
        //accept_button.remove();
        //decline_button.remove();
        //decline_rec(place_id);
        //setTimeout(() => {
          //show_query();
          //scroll_div.scrollTop = scroll_div.scrollHeight;
       // }, 5000); 
    };

    //add buttons to the reccomendation message container
    rec_button_group.appendChild(accept_button);
    rec_button_group.appendChild(decline_button);
    util_button_group.appendChild(block_button);
    util_button_group.appendChild(report_button);
    rec_button_group.appendChild(util_button_group);

    active_rec_message.appendChild(rec_info);
    active_rec_message.appendChild(rec_button_group);

    var message_stack = document.getElementById('message-stack');
    hideQuery();
    message_stack.insertBefore(user_req_message, message_stack.firstChild);
    scroll_div.scrollTop = scroll_div.scrollHeight;
    //sequentially insert the indiviidual messages into the message container and scroll down to the bottom

    setTimeout(() => {
        message_stack.insertBefore(new_message, message_stack.firstChild);
        scroll_div.scrollTop = scroll_div.scrollHeight;
    }, 500); 
    setTimeout(() => {
        message_stack.insertBefore(active_rec_message, message_stack.firstChild);
        var scroll_div = document.querySelector('.scroll');
        scroll_div.scrollTop = scroll_div.scrollHeight;
      }, 1000);

    
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

  function show_query(){
    //show the query container

    document.getElementById('submit_button').style.display = 'inline';

    var submit_elements = document.getElementById('message-form').elements;

    for (var i = 0; i < submit_elements.length; i++) {
      submit_elements[i].disabled = false;
      submit_elements[i].style.visibility = 'visible'; 
    }
    
  }

  function fetch_and_update_active_place(user_id, lat, long,radius, place_type) {
    //passing the parameters call the fetch function in the flask app to get a recommendation
      var url = `/get_new_active_place?user_id=${user_id}&lat=${lat}&long=${long}&radius=${radius}&place_type=${place_type}`;
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

  function accept_rec(place_id) {
    //passing the parameters call the accept function in flask
    var url = `/accept_rec?place_id=${place_id}`;
    return fetch(url)
    .catch(error => {
              console.error('Error:', error);
              throw error;
    });
    //Here is where we would set active place to focus
  }

  function decline_rec(place_id) {
    //passing the parameters call the accept function in flask
    var url = `/decline_rec?place_id=${place_id}`;
    return fetch(url)
    .catch(error => {
              console.error('Error:', error);
              throw error;
    });
    //Here is where we would set active place to focus
  }

  function block_rec(place_id) {
    //passing the parameters call the accept function in flask
    var url = `/block_rec?place_id=${place_id}`;
    return fetch(url)
    .catch(error => {
              console.error('Error:', error);
              throw error;
    });
  }


  function catch_loc_error(error) {
    //this just runs if something happens with the geolocation, create a message asking them to turn it on.
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.log("User denied the request for Geolocation.");
            var mes_content = "Sorry, but without a location, I can't recommend :(, please activate your location services and try again!";
  
            var new_message = document.createElement('div');
            new_message.className = 'message';

            var message_image = document.createElement('img');
            message_image.src = "{{ url_for('static', filename='hango.png') }}";
            message_image.className = 'message-image';

            new_message.appendChild(message_image);
            new_message.appendChild(document.createTextNode(mes_content));

            var message_stack = document.getElementById('message-stack');
            message_stack.insertBefore(new_message, message_stack.firstChild);
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
  //show the additional fields in the query contianer.
  //Edit these how you seem fit, but make sure values are correct
  var selection = document.getElementById("message_type").value;
  var add_field_div = document.getElementById("additional-fields");
  add_field_div.innerHTML = ""; 

  if (selection === "radius" || selection === "type_radius") {
    add_field_div.innerHTML += `
      <label for="radius">Radius (in miles):</label>
      <select id="radius" class="add-selector" name="radius" required>
        <option value="">Please select...</option>
        <option value="5">5 mi</option>
        <option value="10">10 mi</option>
        <option value="20">20 mi</option>
      </select><br>
    `;
  }

  if (selection === "type" || selection === "type_radius") {
    add_field_div.innerHTML += `
      <label for="place_type">Place Type:</label>
      <select id="place_type" class="add-selector" name="place_type" required>
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

function get_user_location(callback){
  //using the navigator interface we can get the gps location of the user using the browser.
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