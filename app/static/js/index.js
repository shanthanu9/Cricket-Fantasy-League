$(document).ready(function() {
    var $matches = $('#matches');

    // Slick Carousal
    $matches.slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 3
    });

    // Socket IO
    var socket = io.connect(`http://${document.domain}:${location.port}`);

    socket.on('matches', function(msg) {
        console.log(msg.matches);
        $matches.slick('unslick');
        $matches.empty();
        for(var i = 0; i < msg.matches.length; i++) {
            match = msg.matches[i];
            console.log('Added match');
            $matches.append(
                `<div class="match card">`+
                    `<p>${match.status}<\p>`+
                    `<p>${match.teams[0].name} : ${match.teams[0].score}</p>`+
                    `<p>${match.teams[1].name} : ${match.teams[1].score}</p>`+
                    `<button match_id="${match.id}" class="make_team">Make team!</button>`+
                `</div>`
                );
        }
        // slick carousal
        $matches.slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 3
        });
    });

    // AJAX request for creating a team
    $(document).on('click', '.make_team', function() { // This syntax because event listener is being added to dynamically created nodes
        var match_id = $(this).attr('match_id');
        // Redirect to relevant URL
        window.location.href = `/myteam?match_id=${match_id}`;
    });
});