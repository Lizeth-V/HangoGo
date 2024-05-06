function expandChatbox() {
    const userProfile = document.querySelector('.user-profile');
    const userChatbox = document.querySelector('.user-chatbox');
    userProfile.classList.toggle('hide-profile');
    userChatbox.classList.toggle('expanded-chatbox');

    const buttCont = document.querySelector('.button-container');
    buttCont.style.marginInline = '0px';
    buttCont.style.marginLeft = '4%';

    buttCont.innerHTML = '<button onclick="returnToDefault()" class="expandProfileBtn" id="expandProfileBtn"><i class="fa-solid fa-chevron-right"></i></button>' +
    '<button onclick="expandChatbox()" class="expandChatboxBtn" id="expandChatboxBtn" style="visibility:hidden"><i class="fa-solid fa-chevron-right"></i></button>';

} 

function expandProfile() {
    const userProfile = document.querySelector('.user-profile');
    const userChatbox = document.querySelector('.user-chatbox');
    userChatbox.classList.toggle('hide-chatbox');
    userProfile.classList.toggle('expanded-profile');

    const buttCont = document.querySelector('.button-container');
    buttCont.style.marginInline = '0px';
    buttCont.style.marginRight = '1%';

    buttCont.innerHTML = '<button onclick="returnToDefault()" class="expandProfileBtn" id="expandProfileBtn"><i class="fa-solid fa-chevron-left"></i></button>' +
    '<button onclick="expandChatbox()" class="expandChatboxBtn" id="expandChatboxBtn" style="visibility:hidden"><i class="fa-solid fa-chevron-right"></i></button>';
}

function returnToDefault(){
    const userProfile = document.querySelector('.user-profile');
    const userChatbox = document.querySelector('.user-chatbox');

    if (userProfile.classList.contains('expanded-profile')) {
        userProfile.classList.remove('expanded-profile');
    }
    if (userChatbox.classList.contains('expanded-chatbox')) {
        userChatbox.classList.remove('expanded-chatbox');
    }
    if (userProfile.classList.contains('hide-profile')) {
        userProfile.classList.remove('hide-profile');
    }
    if (userChatbox.classList.contains('hide-chatbox')) {
        userChatbox.classList.remove('hide-chatbox');
    }
    //toggle hide and expanded off


    const buttCont = document.querySelector('.button-container');
    buttCont.style.marginLeft = '0%';
    buttCont.style.marginRight = '0%';
    buttCont.style.marginInline = '10px';


    buttCont.innerHTML = '<button onclick="expandProfile()" class="expandProfileBtn" id="expandProfileBtn"><i class="fa-solid fa-chevron-right"></i></button>' +
    '<button onclick="expandChatbox()" class="expandChatboxBtn" id="expandChatboxBtn"><i class="fa-solid fa-chevron-left"></i></button>';
}

function addToFavorites(index) {
    console.log("adding to favs")
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