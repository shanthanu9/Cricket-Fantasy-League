$(document).ready(function() {
    var $matches = $('#matches');

    // Socket IO
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('matches', function(msg) {
        console.log(msg.matches);
        $matches.empty();
        $.each(msg.matches, function(i, match) {
            $matches.append(
                `<div class="match">`+
                    `<p>${match.status}<\p>`+
                    `<p>${match.teams[0].name} : ${match.teams[0].score}</p>`+
                    `<p>${match.teams[1].name} : ${match.teams[1].score}`+
                    `<button data-id="${i}">Make team!</button>`+
                `</div>`
                );
        });
        // Slick Carousal
        $matches.slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 3
        });
    });
});