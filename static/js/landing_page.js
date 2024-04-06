function expandChatbox() {
    const userProfile = document.querySelector('.user-profile');
    const userChatbox = document.querySelector('.user-chatbox');
    userProfile.classList.toggle('hide-profile');
    userChatbox.classList.toggle('expanded-chatbox');
} 

function expandProfile() {
    const userProfile = document.querySelector('.user-profile');
    const userChatbox = document.querySelector('.user-chatbox');
    userProfile.classList.toggle('expanded-profile');
    userChatbox.classList.toggle('hide-chatbox');
}

function addToFavorites(index) {
$.ajax({
    url: '/add_to_favorites',
    type: 'POST',
    data: { place_index: index },
    success: function (response) {
    if (response.success) {
        alert(response.message)
    }
}
});
}