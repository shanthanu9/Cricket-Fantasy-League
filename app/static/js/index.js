$(document).ready(function() {
    var $matches = $('#matches');

    // Socket IO
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('matches', function(msg) {
        console.log(msg.matches);
        $matches.empty();
        // $matches.slick('unslick');
        $.each(msg.matches, function(i, match) {
            $matches.append(
                `<div class="match">`+
                    `<p>${match.status}<\p>`+
                    `<p>${match.teams[0].name} : ${match.teams[0].score}</p>`+
                    `<p>${match.teams[1].name} : ${match.teams[1].score}</p>`+
                    `<button match_id="${i}" class="make_team">Make team!</button>`+
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

    // AJAX request for creating a team
    $(document).on('click', '.make_team', function() { // This syntax because event listener is being added to dynamically created nodes
        var match_id = $(this).attr('match_id');
        $.ajax({
            // url: `/myteam?match_id=${match_id}`,
            success: function() {
                window.location.href = `/myteam?match_id=${match_id}`;
            }
        });
    });
});