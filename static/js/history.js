///this gets user id and displays their recommendation history when the open the page.
function fetchUserHistory() {
    var url = `/inflate_user_history`;
    //call flask to recieve feedback history from the past
    //var url = `/inflate_user_history?user_id=${user_id}`;
    //needs user id
    fetch(url)
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
      console.log(data);
      var message_stack = document.getElementById('message-stack');
      var messageHTML = '';
      
    //prints out every recommendation from the past month
      for (let i = 0; i < data.history.length; i++) {
          var userMessage = data.history[i];
          if (userMessage.source === 'hango'){
          var messageElement = `
              <div class="message">  
                  <img src="static/hango.png" class="message-image">
                  ${userMessage.message}
              </div>
          `;
          messageHTML = messageElement + messageHTML;
      }

      else{
        var messageElement = `
              <div class="user-message">  
                ${userMessage.message}  
                <img src="static/user-solid-24.png" class="user-image">
              </div>
          `;
          messageHTML = messageElement + messageHTML;
      }
    }

      message_stack.innerHTML = messageHTML;

    })
    .catch(error => console.error('Error fetching user history:', error));
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

    let original_content;

function switch_history() {
    var elements = document.getElementsByClassName('accept-button');
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }

    var elements = document.getElementsByClassName('decline-button');
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }

    var elements = document.getElementsByClassName('block-button');
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }

    var elements = document.getElementsByClassName('report-button');
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }


    if (!original_content) {
        original_content = document.querySelector(".container.mt-5").innerHTML;
    }
    document.querySelector(".container.mt-5").innerHTML = '<img type="button" id="back-button" class="back-button" title="Return" src="static/chevron-left-square-regular-40.png" onclick="switch_restore()" /> <img type="button" id="del-button" class="del-button" title="Delete History" onclick="delete_user_chat_history()" src="static/trash-alt-regular-36.png"/><div class="chatbox"><div class="messages" id="messages"><div class="scroll" class="scroll"><div id="message-stack" class="message-stack"></div></div></div></div>';

    fetchUserHistory()
}

function switch_restore(){
    if (original_content){
        document.querySelector(".container.mt-5").innerHTML = original_content;

        show_query();

        //reattach the event listener
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

        original_content = undefined
    }
}

function delete_user_chat_history(){
    var url = '/delete_user_chats?user_id=${user_id}';

    //popup confirmation
    if (confirm("Are you sure you want to delete your chat history? It cannot be recovered.")) {
        document.querySelector(".container.mt-5").innerHTML = '<img type="button" id="back-button" class="back-button" title="Return" src="static/chevron-left-square-regular-40.png" onclick="switch_restore()" /> <img type="button" id="del-button" class="del-button" title="Delete History" onclick="delete_user_chat_history()" src="static/trash-alt-regular-36.png"/><div class="chatbox"><div class="messages" id="messages"><div class="scroll" class="scroll"><div id="message-stack" class="message-stack"></div></div></div></div>';
        fetch(url);
    } else {
        // User canceled the deletion
        console.log("Deletion canceled by user.");
    }}

//window.onload = fetchUserHistory();