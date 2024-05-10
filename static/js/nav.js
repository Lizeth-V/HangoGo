var profile_html;

function fetch_active_place(user_id) {
    var url = `/fetch_user_active_place?user_id=${user_id}`;

    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

function loadFavorites() {
    fetch(`/favorites?`)
    .then(response => response.json())
    .then(data => {
        const favoritesContainer = document.getElementById('userProfileContainer');
        favoritesContainer.innerHTML = '';

        const favoriteScroll = document.createElement('container');
        favoriteScroll.classList.add('scroll');

        const favoriteh1 = document.createElement('div');
        favoriteh1.innerHTML = `
            <h1>Favorites</h1>
        `;
        favoriteScroll.appendChild(favoriteh1);

        data.favorites.forEach(favorite => {
            const favoriteDiv = document.createElement('div');
            favoriteDiv.className = 'favorite';
            favoriteDiv.innerHTML = `
                <img src="${favorite.icon}" alt="Icon">
                <div>
                    <p>${favorite.name}</p>
                    <p>${favorite.address}</p>
                    <button type="button" class="btn btn-success" onclick="setActive('${favorite.place_id}')">visit</button>
                    <button type="button" class="btn btn-danger" onclick="deleteFavorite('${favorite.place_id}')">delete</button>
                    </div>
            `;
            favoriteScroll.appendChild(favoriteDiv);
        });

        favoritesContainer.appendChild(favoriteScroll);
        //button adjust
        const map_button = document.getElementById('map_button');
        map_button.innerHTML = '<a onclick="changeToMap()"><i class="bx bxs-map-pin icon"></i></a>';

        const user_profile_button = document.getElementById('user_p_button');
        user_profile_button.innerHTML = '<a onclick="change_to_profile()"><i class="bx bxs-user-detail icon"></i></a>';

        const fav_button = document.getElementById('fav_button');
        fav_button.innerHTML = '<a><i class="bx bxs-buildings icon"></i></a>';
    });
}

function deleteFavorite(place_id){
    var url = `/remove_from_favorites?place_id=${place_id}`;
  
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            window.alert("Place removed from favorites.");
            loadFavorites()
            return 'Success'
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to remove active place: ' + error.message);
        });
}

function setActive(place_id) {
    var url = `/set_user_active_place?place_id=${place_id}`;
  
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            changeToMap();
            return 'Success'
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to set acgtive place: ' + error.message);
        });
}

function changeToMap(user_id, place_name, place_address, place_coordinates, user_coordinates, place_id) {
    if (place_name == undefined){

        get_user_location(function(position) {
            latitude = position.latitude;
            longitude = position.longitude;

            fetch_active_place(user_id)
            .then(data => { 
                if (data.name != undefined){
                        place_name = data.name;
                        user_coordinates = latitude + "," + longitude;
                        place_coordinates = data.lat + "," + data.lon;
                        place_address = data.address;
                        place_id = data._id;

                        var distance = calculateDistance(user_coordinates, place_coordinates);

                        const user_profile_container = document.getElementById('userProfileContainer');

                        user_profile_container.innerHTML = '';

                        // Clear existing content if necessary
                        // user_profile_container.innerHTML = ''; // Uncomment only if you need to reset the content
                    
                        const map_div = document.createElement('div');
                        map_div.className = 'map';
                    
                        const iframe = document.createElement('iframe');
                        iframe.width = '90%';
                        iframe.height = '50%';
                        iframe.frameBorder = '0';
                        iframe.style.border = '0';
                        iframe.loading = 'lazy';
                        iframe.referrerPolicy = 'no-referrer-when-downgrade';
                        // Uncomment and set src as needed
                        iframe.src = 'https://www.google.com/maps/embed/v1/directions?key=AIzaSyDC1Ysg0I0IHqCs_TDxFwkMJDK71zruEGk&origin='+ user_coordinates + '&destination=' + place_address + '&avoid=tolls|highways';
                        map_div.appendChild(iframe);
                    
                        const h1 = document.createElement('h1');
                        h1.textContent = place_name;
                        map_div.appendChild(h1);
                    
                        const p_address = document.createElement('p');
                        p_address.textContent = place_address;
                        map_div.appendChild(p_address);
                    
                        const p_distance = document.createElement('p');
                        p_distance.textContent = `Distance: ${distance} km`;
                        map_div.appendChild(p_distance);
                    
                        const buttons_div = document.createElement('div');
                        buttons_div.className = 'map-buttons';
                    
                        const favorite_button_div = document.createElement('div');
                        favorite_button_div.className = 'favorite-map-button';
                        favorite_button_div.setAttribute('onClick', `add_favorite('${place_id}')`);
                        favorite_button_div.innerHTML = '<img src="static/star-regular-48.png"/><h1>favorite</h1>';
                        buttons_div.appendChild(favorite_button_div);
                    
                        const remove_button_div = document.createElement('div');
                        remove_button_div.className = 'remove-map-button';
                        remove_button_div.setAttribute('onClick', `remove_active('${user_id}')`);
                        remove_button_div.innerHTML = '<img src="static/x-circle-solid-48.png"/><h1>remove</h1>';
                        buttons_div.appendChild(remove_button_div);
                    
                        map_div.appendChild(buttons_div);
                    
                        user_profile_container.appendChild(map_div);

                        const map_button = document.getElementById('map_button');
                        map_button.innerHTML = '<a><i class="bx bxs-map-pin icon"></i></a>';

                        const user_profile_button = document.getElementById('user_p_button');
                        user_profile_button.innerHTML = '<a onclick="change_to_profile()"><i class="bx bxs-user-detail icon"></i></a>';

                        const fav_button = document.getElementById('fav_button');
                        fav_button.innerHTML = '<a onclick="loadFavorites()"><i class="bx bxs-buildings icon"></i></a>';


                        }
                else{
                    const container = document.getElementById('userProfileContainer');

                    container.innerHTML = '';

                    const map_div = document.createElement('div');
                    map_div.className = 'map';

                    const iframe = document.createElement('iframe');
                    iframe.width = '90%';
                    iframe.height = '50%';
                    iframe.frameBorder = '0';
                    iframe.style.border = '0';
                    iframe.referrerPolicy = 'no-referrer-when-downgrade';
                    // Uncomment to set the src attribute dynamically
                    iframe.src = `https://www.google.com/maps/embed/v1/place?key=AIzaSyDC1Ysg0I0IHqCs_TDxFwkMJDK71zruEGk&q=${encodeURIComponent(latitude + "," + longitude)}`;
                    map_div.appendChild(iframe);

                    const header = document.createElement('h1');
                    header.textContent = 'No Active Place';
                    map_div.appendChild(header);

                    container.appendChild(map_div);

                    const map_button = document.getElementById('map_button');
                    map_button.innerHTML = '<a><i class="bx bxs-map-pin icon"></i></a>';

                    const user_profile_button = document.getElementById('user_p_button');
                    user_profile_button.innerHTML = '<a onclick="change_to_profile()"><i class="bx bxs-user-detail icon"></i></a>';

                    const fav_button = document.getElementById('fav_button');
                    fav_button.innerHTML = '<a onclick="loadFavorites()"><i class="bx bxs-buildings icon"></i></a>';
                    }
                }
                )
            .catch(error => {
                // Handle any errors that occurred during fetch_active_place
                console.error("Error fetching active place:", error);
            });

         });
    }

    else{
        const user_profile_container = document.getElementById('userProfileContainer');
        var distance = calculateDistance(user_coordinates, place_coordinates);

        //Clear container
        user_profile_container.innerHTML = '';

        const map_div = document.createElement('div');
        map_div.className = 'map';

        const iframe = document.createElement('iframe');
        iframe.width = '90%';
        iframe.height = '50%';
        iframe.frameBorder = '0';
        iframe.style.border = '0';
        iframe.loading = 'lazy';
        iframe.referrerPolicy = 'no-referrer-when-downgrade';
        // Uncomment and set src as needed
        iframe.src = 'https://www.google.com/maps/embed/v1/directions?key=AIzaSyDC1Ysg0I0IHqCs_TDxFwkMJDK71zruEGk&origin='+ user_coordinates + '&destination=' + place_address + '&avoid=tolls|highways';
        map_div.appendChild(iframe);

        const h1 = document.createElement('h1');
        h1.textContent = place_name;
        map_div.appendChild(h1);

        const p_address = document.createElement('p');
        p_address.textContent = place_address;
        map_div.appendChild(p_address);

        const p_distance = document.createElement('p');
        p_distance.textContent = `Distance: ${distance} km`;
        map_div.appendChild(p_distance);

        const buttons_div = document.createElement('div');
        buttons_div.className = 'map-buttons';

        const favorite_button_div = document.createElement('div');
        favorite_button_div.className = 'favorite-map-button';
        favorite_button_div.setAttribute('onClick', `add_favorite('${place_id}')`);

        favorite_button_div.innerHTML = '<img src="static/star-regular-48.png"/><h1>favorite</h1>';
        buttons_div.appendChild(favorite_button_div);

        const remove_button_div = document.createElement('div');
        remove_button_div.className = 'remove-map-button';
        remove_button_div.setAttribute('onClick', `remove_active('${user_id}')`);
        remove_button_div.innerHTML = '<img src="static/x-circle-solid-48.png"/><h1>remove</h1>';
        buttons_div.appendChild(remove_button_div);

        map_div.appendChild(buttons_div);

        user_profile_container.appendChild(map_div);   

        const map_button = document.getElementById('map_button');
        map_button.innerHTML = '<a><i class="bx bxs-map-pin icon"></i></a>';

        const user_profile_button = document.getElementById('user_p_button');
        user_profile_button.innerHTML = '<a onclick="change_to_profile()"><i class="bx bxs-user-detail icon"></i></a>';

        const fav_button = document.getElementById('fav_button');
        fav_button.innerHTML = '<a onclick="loadFavorites()"><i class="bx bxs-buildings icon"></i></a>';

        
    }
}

//haversine formula, find distance over sphere (Earth)
function calculateDistance(coords1, coords2) {
    var [lat1, lon1] = coords1.split(',').map(Number);
    var [lat2, lon2] = coords2.split(',').map(Number);

    var R = 6371; // Radius of the Earth in km
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLon = (lon2 - lon1) * Math.PI / 180;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var distance = R * c;

    return distance.toFixed(2);
}

function save_prof(){
    profile_html = document.getElementById('userProfileContainer').innerHTML;
}

function change_to_profile() {

    document.getElementById('map_button').innerHTML = `<a onclick="changeToMap('')"><i class="bx bxs-map-pin icon"></i></a>`;
    document.getElementById('user_p_button').innerHTML = '<a><i class="bx bxs-user-detail icon"></i></a>';
    document.getElementById('fav_button').innerHTML = `<a onclick="loadFavorites()"><i class="bx bxs-buildings icon"></i></a>`;


    document.getElementById('userProfileContainer').innerHTML = profile_html;

}

function remove_active() {
    var url = `/remove_user_active_place`;
  
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            changeToMap();
            return 'Success'
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to remove active place: ' + error.message);
        });
}

function add_favorite(place_id) {
    if (place_id === undefined) {
        fetch_active_place()
        .then(data => {
            place_id = data._id
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to remove active place: ' + error.message);
        });
    }

    var url = `/add_to_favorites2?place_id=${place_id}`;
  
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            window.alert("Place added to favorites!");
            return 'Success'
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to remove active place: ' + error.message);
        });


}
