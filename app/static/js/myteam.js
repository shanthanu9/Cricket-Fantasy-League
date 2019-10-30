$(document).ready(function() {

    var player_count = 0;
    var players_chosen = [];
    const max_players = 11;

    const url = new URL(window.location.href);
    var match_id = url.searchParams.get('match_id');
    console.log(match_id)

    // Socket IO
    var socket = io.connect(`http://${document.domain}:${location.port}`);
    
    socket.on('connect', function() {
        console.log('Request team details');
        socket.emit('get_match', {data: match_id});
    });

    socket.on('match', function(msg) {
        console.log('Fetched team details');
        let teams = msg.match.teams;
        for(let i = 0; i < teams.length; i++) {
            let team = teams[i];
            for(let player_id = 0; player_id < team.length; player_id++) {
                player = team[player_id];
                console.log(player)
                $(`#team-${i+1}`).append(
                    `<button class="select example_e" id="team-${i}-player-${player_id}" data-id="${player.id}">${player.name}</button>`
                );
            }
        }
    });

    // Selecting players
    $(document).on('click', '.select', function() {
        if(player_count >= max_players)
            return;
        player_count++;
        players_chosen.push($(this).attr('data-id'))
        $('#chosen').append(
            `<button class="deselect example_e" id="${$(this).attr('id')}">${$(this).text()}</button>`
        );
        $(this).attr('disabled', true);
    });

    // Removing players
    $(document).on('click', '.deselect', function() {
        player_count--;
        players_chosen = players_chosen.filter(item => item != $(`#${$(this).attr('id')}`).text);
        $(`#${$(this).attr('id')}`).attr('disabled', false);
        $(this).remove();
    });

    // Submit players
    $(document).on('click', '#submit-button', function() {
        console.log('Submit my team!')
        var myteam = {
            match_id: match_id,
            player_count: player_count,
            players: JSON.stringify(players_chosen)
        };

        $.ajax({
            type: 'POST',
            url: '/createteam',
            data: myteam,
            traditional: true,
            success: function() {
                window.location.href = '/index';
            }
        });
    });

});