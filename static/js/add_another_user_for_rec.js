document.addEventListener('DOMContentLoaded', function() {
    const friendsContainer = document.getElementById('friendsContainer');
    const addFriendBtn = document.getElementById('addFriendBtn');
    const friendForm = document.getElementById('friendForm');

    addFriendBtn.addEventListener('click', function() {
        const friendInput = document.createElement('div');
        friendInput.innerHTML = `
            <label for="username"><b>username</b></label><br>
            <input type="text" name="friendName[]" placeholder="Enter Friend's Name">
            <label for="location"><b>location</b></label><br>
            <input type="text" name="friendLocation[]" placeholder="Enter Friend's Location">
        `;
        friendsContainer.appendChild(friendInput);
    });

    friendForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(friendForm);
        const entries = formData.entries();
        const locations = [];

        for (const pair of entries) {
            const [name, value] = pair;
            locations.push({ [name]: value });
        }

        // Send locations data to server for center calculation
        fetch('/calculate_center', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ locations }),
        })
        .then(response => response.json())
        .then(data => {
            // Handle center location response
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});





/*
// org form
document.getElementById('addFriendForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const user = {
        user_name: formData.get('userName'),
        user_location: formData.get('userLocation')
    };
    fetch('/add_another_user_for_rec', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});
*/
document.getElementById('recommendationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const targetUserId = formData.get('targetUserId');
    fetch('/multi_recommendation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({target_user_id: targetUserId})
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = "<h3>Recommendations:</h3>";
        data.recommendations.forEach(recommendation => {
            recommendationsDiv.innerHTML += "<p>" + recommendation + "</p>";
        });
    })
    .catch(error => console.error('Error:', error));
});