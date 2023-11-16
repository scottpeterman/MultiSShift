$(document).ready(function() {
  var authToken = null; // Variable to store the JWT token
  var isLoggedIn = false; // Track if the user is logged in

  // Open the API login modal or DataTable modal based on login status
  $('#selectDevice').click(function() {
    if (!isLoggedIn) {
      $('#apiLoginModal').modal('show');
    } else {
      $('#deviceModal').modal('show');
    }
  });

  // Handle the API login form submission
  $('#apiLoginSubmit').click(function() {
    var username = $('#apiUsername').val();
    var password = $('#apiPassword').val();

    // Perform the API login
    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:8008/login',
      data: { username: username, password: password },
      success: function(data) {
        // Store the JWT token
        authToken = data.access_token;
        isLoggedIn = true; // Set the login status

        // Close the login modal
        $('#apiLoginModal').modal('hide');
        console.log("API login successful");

        // Now load the DataTable with the authenticated session
        loadDataTable();
      },
      error: function() {
        alert("Login failed, please try again.");
      }
    });
  });


  function loadDataTable() {
    if (!authToken) {
      console.error('Authentication token is not available.');
      return;
    }
    $('#deviceModal').modal('show');
    // Initialize DataTable here after successful login
    $('#deviceTable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:8008/api/v1/devices/?skip=0&limit=5000",
        "type": "GET",
        "beforeSend": function(request) {
          request.setRequestHeader("Authorization", authToken);
        },
        "dataSrc": "" // Depending on the format of your response
      },
      "columns": [ // Define columns to match your schema, excluding 'credsid'
    { "data": "id" },
    { "data": "name" },
    { "data": "devicerole" },
    { "data": "mgmtIP" },
    { "data": "subTypeName" },
    { "data": "vendor" },
    { "data": "model" },
    { "data": "ver" },
    { "data": "sn" },

    // Exclude 'credsid' column from here
  ],

    });
  }
});


document.addEventListener('DOMContentLoaded', function() {
  // Get the table body element
  var tableBody = document.querySelector('#deviceTable tbody');

  // Event delegation
  tableBody.addEventListener('click', function(event) {
    // Check if the clicked element is a row
    var target = event.target;
    while (target && target.nodeName !== 'TR') {
      target = target.parentElement;
    }
    if (target) {
      // Get the data from the clicked row
      var cells = target.getElementsByTagName('td');
      // Assuming that the Management IP is in the fourth cell (index 3)
      var managementIp = cells[3].textContent;

      // Log or do something with the managementIp
      console.log(managementIp);

      // Example: populate the input field
      document.getElementById('hostname').value = managementIp;
      $('#deviceModal').modal('hide');
    }
  });
});
