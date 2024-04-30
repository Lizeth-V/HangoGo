

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const map = new Map(document.getElementById("map"), {
      center: { lat: 34.052235, lng: -118.243683 },
      zoom: 11,
      mapId: "4504f8b37365c3d0",
    });

    const devFaves = [
        {
            position: {lat:33.836288015438605, lng: -118.31201931710113},
            title: "Cafe Bene",
        }
    ]
 

    // Function to add markers
    // This works but for now is mainly hard coded to add multiple places - GOAL: Make it work dynamically. 
    function addMarker(position, title, map) {
        const hangoMarkerImg = document.createElement("img");
        hangoMarkerImg.src = "../static/icons/marker.png";

        // Set the size of the marker image
        hangoMarkerImg.style.width = "50px"; // Change the width as needed
        hangoMarkerImg.style.height = "50px"; // Change the height as needed

        const marker = new AdvancedMarkerElement({
            map,
            position,
            content: hangoMarkerImg,
            title,
        });

        // Create an info window
        const infoWindow = new google.maps.InfoWindow({
            content: `<div><strong>${title}</strong><br>Latitude: ${position.lat}<br>Longitude: ${position.lng}</div>`
        });

        // Add event listener for marker mouseover
        marker.addListener('mouseover', () => {
            infoWindow.open(map, marker);
        });

        // Add event listener for marker mouseout
        marker.addListener('mouseout', () => {
            infoWindow.close();
        });

        // Return the marker in case you need to access it later
        return marker;
    }

    // Custom List for Developers Favorites
    addMarker({ lat: 34.0285093, lng: -118.4873733 }, "Hango Marker", map);
    addMarker({ lat: 34.052235, lng: -118.243683 }, "Hango Marker", map);
}

initMap();
