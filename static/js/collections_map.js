

async function initMap(placeData) {
    const { Map, InfoWindow } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const map = new Map(document.getElementById("map"), {
      center: { lat: 33.94021447565573, lng: -118.13785340521298 },
      zoom: 10,
      mapId: "4504f8b37365c3d0",
    });

    let openInfoWindow = null;

    // Function to add markers
    // This works but for now is mainly hard coded to add multiple places - GOAL: Make it work dynamically. 
    function addMarker(position, name, map) {
        const hangoMarkerImg = document.createElement("img");
        hangoMarkerImg.src = "../static/icons/marker.png";

        hangoMarkerImg.style.width = "50px"; 
        hangoMarkerImg.style.height = "50px"; 

        const marker = new AdvancedMarkerElement({
            map,
            position,
            content: hangoMarkerImg,
            title: name,
        });

        const infoWindowContent = `
            <div style="text-align: center; color: #5EBA47;">
                <h4>${name}</h4>
            </div>
        `;

        // Create info window
        const infoWindow = new InfoWindow({
            content: infoWindowContent,
        });
        //marker can be opened one at a time
        marker.addListener("click", () => {

            if (openInfoWindow) {
                openInfoWindow.close();
            }
            infoWindow.open(map, marker);
            openInfoWindow = infoWindow;
        });


    }


    // Loop through place coordinates and add markers
    placeData.forEach(place => {
        addMarker(place.coordinates, place.name, map);
    });

}

initMap(placeData);
