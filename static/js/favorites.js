function openNav() {
    document.getElementById("mySidebar").style.width = "50vw";
    document.getElementById("main").style.marginLeft = "250px";
}
  
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
}

$(document).ready(function(){
    $('.del-favorite').click(function(){
        var place_id = $(this).data('place-id');
        $.ajax({
            url: '/remove_from_favorites',
            type: 'POST',
            data: {place_id: place_id},
            success: function(response) {
                if (response.success) {
                    // If removal was successful, remove the entire div containing the place details
                    var placeDiv = document.getElementById(place-{ place_id });
                    console.log(place_id);
                    if (placeDiv) {
                        placeDiv.parentNode.removeChild(placeDiv);
                        alert(response.message); // Optional: Show a message indicating success
                    } else {
                        alert('Failed to find place to remove.'); // Show an error message if the div is not found
                    }
                }
            }
                
            // error: function(xhr, status, error) {
            //     console.error(xhr.responseText); // Log the error in the console
            //     alert('Error: ' + xhr.responseText); // Optional: Show an error message
            // }
        });
    });
});