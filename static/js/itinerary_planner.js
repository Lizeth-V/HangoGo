$(document).ready(function() {
    // Add place
    $("#addPlace").click(function() {
        var placeName = $("input[name='name']").val();
        if (placeName) {
            $("#placesList").append(
                '<div><input type="checkbox" name="places" value="' + placeName + '">' + placeName + '</div>'
            );
        }
    });

    // Remove place
    $(document).on("click", "input[type='checkbox']", function() {
        $(this).parent().remove();
    });

    // Plan Trip
    $("#planTrip").click(function() {
        $.ajax({
            type: "POST",
            url: "/plan_trip",
            data: $("#placeForm").serialize(),
            success: function(response) {
                console.log(response);
            }
        });
    });
});