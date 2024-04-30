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