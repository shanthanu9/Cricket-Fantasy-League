$(document).ready(function() {


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
                    `<button class="select example_e" id="team-${i}-player-${player_id}">${player.name}</button>`
                );
            }
        }
    });

    // Selecting players
    $(document).on('click', '.select', function() {
        $('#chosen').append(
            `<button class="deselect example_e" id="${$(this).attr('id')}">${$(this).text()}</button>`
        );
        $(this).attr('disabled', true);
    });

    // Removing players
    $(document).on('click', '.deselect', function() {
        $(`#${$(this).attr('id')}`).attr('disabled', false);
        $(this).remove();
    });
});