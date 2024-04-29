var topPlaces = {{ top_places | tojson }};

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const map = new Map(document.getElementById("map"), {
      center: { lat: 34.052235, lng: -118.243683 },
      zoom: 11,
      mapId: "4504f8b37365c3d0",
    });



    async function getPlacesAddMarkers(){
        try{
            const response = await fetch('/cafe_culture');
            const places = await response.json();
            places.forEach(place => {
                const marker = new google.maps.Marker({
                    position: { lat: place.lat, lng: place.lon },
                    map: map,
                    title: place.title
                });
            });
        } catch (error) {
            console.error('Error:', error);
        }
    }
    await getPlacesAndAddMarkers();


    

    // // Function to add markers
    // function addMarker(position, title, map) {
    //     const hangoMarkerImg = document.createElement("img");
    //     hangoMarkerImg.src = "../static/icons/marker.png";

    //     // Set the size of the marker image
    //     hangoMarkerImg.style.width = "50px"; // Change the width as needed
    //     hangoMarkerImg.style.height = "50px"; // Change the height as needed

    //     const marker = new AdvancedMarkerElement({
    //         map,
    //         position,
    //         content: hangoMarkerImg,
    //         title,
    //     });
    // }

    // // Example markers
    // addMarker({ lat: 34.0285093, lng: -118.4873733 }, "Hango Marker", map);
    // addMarker({ lat: 34.052235, lng: -118.243683 }, "Another Marker", map);
}

initMap();
