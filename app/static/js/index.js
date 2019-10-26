$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('matches', function(msg) {
        console.log(msg.matches)
        $('#matches').empty();
        for (const match of msg.matches) {
            $('#matches').append('<li>'+match+'</li>')
        }
        console.log(msg.leagues)    
    });
});