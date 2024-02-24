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
    console.log('Cancel Edit Mode called');

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

// Saves users new changes and updates the database
function saveDetails() {
    console.log('Save Details Function called');
    // Prepare the data to be sent to the server for updating MongoDB
    const userId = document.getElementById('userId').value; 

    const updatedDetails = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        email: document.getElementById('email').value,
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

            // Revert back to the original styling when saving details
            var editableElements = document.querySelectorAll('.editable');
            editableElements.forEach(function (element) {
                element.classList.remove('editing-mode');
                console.log('Removed editing-mode class:', element);
            });

            // Shows Edit button - hides save and cancel buttons
            document.getElementById('editButton').style.display = 'inline-block';
            document.getElementById('saveButton').style.display = 'none';
            document.getElementById('cancelButton').style.display = 'none';
        },
        error: function (error) {
            console.error('Error updating user details:', error);
            // Handle the error as needed
        },
    });

        
}

function createInputField(value, id) {
    var input = document.createElement('input');
    input.type = 'text';
    input.value = value;
    input.id = id;
    return input;
}