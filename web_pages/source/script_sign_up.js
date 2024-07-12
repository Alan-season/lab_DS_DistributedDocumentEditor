$(document).ready(function() {
    $('#usernameForm').on('submit', function(event) {
        event.preventDefault();
        var user_name = $('#user_name').val();
        $.ajax({
            type: 'POST',
            url: '/sign_up_submit',
            data: JSON.stringify({user_name: user_name}),
            contentType: 'application/json',
            success: function(response) {
                console.log('Username signed up: ', response.user_name);
                window.location.href = '/';
            }
        });
    });
});

window.addEventListener('beforeunload', function (e) {
    navigator.sendBeacon('/shutdown');
});