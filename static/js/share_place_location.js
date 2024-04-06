// Function to retrieve a place from the database using its ID
async function getPlace(placeId) {
    // Send a request to the server to retrieve the place data
    const response = await fetch('/get_place', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `place_id=${placeId}`
    });
    // Parse the response data as JSON and return it
    const data = await response.json();
    return data;
}

// Function to share a place
function sharePlace(placeId) {
    // Get the URL of the place from the HTML element
    const placeLink = document.querySelector(`#place-${placeId} .place-link`).innerText;

    // Define the sharing options
    const shareOptions = {
        text: `Check out this place: ${placeLink}`,
        url: placeLink
    };

    // Check if the Web Share API is available
    if (navigator.share) {
        // Use the Web Share API to share the place
        navigator.share(shareOptions);
    } else {
        // Fallback for browsers that do not support the Web Share API
        // Create a temporary text area element to copy the URL to the clipboard
        const shareText = `Check out this place: ${placeLink}`;
        const textArea = document.createElement('textarea');
        textArea.value = shareText;
        document.body.appendChild(textArea);
        textArea.select();
        // Copy the text to the clipboard
        document.execCommand('copy');
        document.body.removeChild(textArea);
        // Show an alert to indicate that the URL has been copied
        alert('Place URL copied to clipboard');
    }
}