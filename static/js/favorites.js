function expandChatbox() {
    const favoritesList = document.querySelector('.favorites-list');
    const userChatbox = document.querySelector('.user-chatbox');
    favoritesList.classList.toggle('hide-favorites');
    userChatbox.classList.toggle('expanded-chatbox');
} 

function expandFavorites() {
    const favoritesList = document.querySelector('.favorites-list');
    const userChatbox = document.querySelector('.user-chatbox');
    favoritesList.classList.toggle('expanded-favorites');
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