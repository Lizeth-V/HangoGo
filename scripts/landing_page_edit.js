function enableEditMode() {
    // elements being edited - birthday is not allowed to be edited 
    var firstName = document.getElementById('first_name');
    var lastName = document.getElementById('last_name');
    var email = document.getElementById('email');

    // create input fields for editing
    var inputFirstName = createInputField(firstName.innerText, 'first_name');
    var inputLastName = createInputField(lastName.innerText, 'last_name');
    var inputEmail = createInputField(email.innerText, 'email');

    // Replace text with input fields
    firstName.innerHTML = '';  // Clears existing content
    firstName.appendChild(inputFirstName);
    
    lastName.innerHTML = '';  
    lastName.appendChild(inputLastName);

    email.innerHTML = '';
    email.appendChild(inputEmail);

    // Shows only the save and cancel buttons
    document.getElementById('editButton').style.display = 'none';
    document.getElementById('saveButton').style.display = 'inline-block';
    document.getElementById('cancelButton').style.display = 'inline-block'
}
// Cancel Edit Mode
function cancelEditMode() {

var firstName = document.getElementById('first_name');
var lastName = document.getElementById('last_name');
var email = document.getElementById('email');

// revert to original content
firstName.innerHTML = '{{first_name}}';
lastName.innerHTML = '{{last_name}}';
email.innerHTML = '{{email}}';

// Shows Edit button - hides save and cancel buttons
document.getElementById('editButton').style.display = 'inline-block';
document.getElementById('saveButton').style.display = 'none';
document.getElementById('cancelButton').style.display = 'none';
}

// saves users new changes and updates the database
function saveDetails() {
// Prepare the data to be sent to the server for updating MongoDB
const userId = 'replace-with-the-actual-user-id'; // Replace with the actual user ID
const updatedDetails = {
    first_name: document.getElementById('first_name').textContent,
    last_name: document.getElementById('last_name').textContent,
    email: document.getElementById('email').textContent,
};

// Makes an AJAX request to update user details in MongoDB
$.ajax({
    url: '/update-user',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ userId, updatedDetails }),
    success: function (response) {
    console.log('User details updated:', response);

    // Update the displayed user details with the updated data
    document.getElementById('first_name').textContent = response.first_name;
    document.getElementById('last_name').textContent = response.last_name;
    document.getElementById('email').textContent = response.email;

    
    },
    error: function (error) {
    console.error('Error updating user details:', error);
    
    },
});

// Reverts back to the original styling when saving details
var editableElements = document.querySelectorAll('.editable');
editableElements.forEach(function (element) {
    element.classList.remove('editing-mode');
});

// Shows Edit button - hides save and cancel buttons
document.getElementById('editButton').style.display = 'inline-block';
document.getElementById('saveButton').style.display = 'none';
document.getElementById('cancelButton').style.display = 'none';
}

function createInputField(value, id) {
    var input = document.createElement('input');
    input.type = 'text';
    input.value = value;
    input.id = id;
    return input;
}