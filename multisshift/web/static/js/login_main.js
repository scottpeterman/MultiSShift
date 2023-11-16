        authToken = null;
        isLoggedIn = false; // Set the login status

    function btnLogin() {
    event.preventDefault(); // Prevent the immediate navigation

    // Get username and password from the form
    var username = $('#signin-email').val();
    var password = $('#signin-password').val();

    // Show the loading overlay
    document.getElementById('loadingOverlay').style.display = 'flex';

    // Perform the API login
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8008/login', // Replace with your API's login endpoint
        data: { username: username, password: password },
        success: function(data) {

            // You might want to redirect the user or load new content here
            console.log("API login successful");
            authToken = data.access_token;
            isLoggedIn = true; // Set the login status
            // After successful API login, submit the form (if needed)
            setTimeout(function() {
                document.getElementById('login_form').submit();
            }, 500);
        },
        error: function(jqXHR, textStatus, errorThrown) {
        // Handle login failure
        var errorMessage = "Login failed: ";
        if (jqXHR.responseJSON && jqXHR.responseJSON.detail) {
            // If the server sends a specific error message
            errorMessage += jqXHR.responseJSON.detail;
        } else {
            // Default to a generic error message
            errorMessage += "An error occurred. Please try again.";
        }

        // Display the error message
        alert(errorMessage);
        console.error("Error details:", textStatus, errorThrown);

        // Hide overlay on failure
        document.getElementById('loadingOverlay').style.display = 'none';
    }
    });
}