function enableEditMode() {
    console.log('Edit Mode enabled');
    // elements being edited - birthday is not allowed to be edited 
    // Show input fields and buttons
    document.getElementById('edit_first_name').style.display = 'block';
    document.getElementById('edit_last_name').style.display = 'block';
    document.getElementById('edit_email').style.display = 'block';
    
    // Hide the original paragraphs
    document.getElementById('first_name').style.display = 'none';
    document.getElementById('last_name').style.display = 'none';
    document.getElementById('email').style.display = 'none';
    
    // Show the Save Changes button
    document.getElementById('editButton').style.display = 'none';
    document.querySelector('button[type="submit"]').style.display = 'inline-block';
    document.getElementById('cancelButton').style.display = 'inline-block';
}

// Cancel Edit Mode
function cancelEditMode() {
    console.log('Cancel Edit Mode called');

    // hiding input boxes and show original paragraphs
    document.getElementById('edit_first_name').style.display = 'none';
    document.getElementById('edit_last_name').style.display = 'none';
    document.getElementById('edit_email').style.display = 'none';
    
    document.getElementById('first_name').style.display = 'block';
    document.getElementById('last_name').style.display = 'block';
    document.getElementById('email').style.display = 'block';
    
    // hiding the Save Changes and Cancel buttons
    document.getElementById('editButton').style.display = 'inline-block';
    document.querySelector('button[type="submit"]').style.display = 'none';
    document.getElementById('cancelButton').style.display = 'none';
}

// switching between the profile details conatiner and other 
function toggleDetails(){
    var userProfileContainer = document.getElementById('userProfileItems');
    var moreChoicesContainer = document.getElementById('moreChoicesContainer');

    if (userProfileContainer.style.display !== 'none') {
    // hiding profile details to show other content 
    userProfileContainer.style.display = 'none';
    moreChoicesContainer.style.display = 'block';
    } 
    else {
    // hiding other content and displaying profile again
    console.log('wtf')
    userProfileContainer.style.display = 'block';
    moreChoicesContainer.style.display = 'none';
    }
}

// Option for user to delete account 
function delete_acct(){
    var confirmDelete = confirm("Are you sure you want to delete your account?");
    if (confirmDelete){
        document.forms[0].submit(); 
    }
}