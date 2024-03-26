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
          var messageElement = `
              <div class="user-message">  
                  ${userMessage}
                  <img src="static\hango.png" class="user-image">
              </div>
          `;
          messageHTML = messageElement + messageHTML;
      }

      message_stack.innerHTML = messageHTML;

    })
    .catch(error => console.error('Error fetching user history:', error));
}

 //DEPRECATED
     /* function save_user_chat(user_id, radius, place_type, place_name, user_action) {
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
      }*/


//window.onload = fetchUserHistory();