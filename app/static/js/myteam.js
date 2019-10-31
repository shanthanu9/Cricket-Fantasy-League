$(document).ready(function() {

    var player_count = 0;
    var players_chosen = [];
    const max_players = 11;
    var score = $('#score').text();

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
        $('#team-1').empty();
        $('#team-2').empty();
        let teams = msg.match.teams;
        for(let i = 0; i < teams.length; i++) {
            let team = teams[i]['roster'];
            $(`#team-${i+1}`).append(
                `<div class="teamName" style="text-align:left">${teams[i]['teamname']}</div>`
            );
            for(let player_id = 0; player_id < team.length; player_id++) {
                player = team[player_id];
                console.log(player)
                $(`#team-${i+1}`).append(
                    `<button class="select example_e" id="team-${i}-player-${player_id}" data-id="${player.id}" score="${player.score}">${player.name} : ${player.score}</button>`
                );
            }
        }
    });

    // Selecting players
    $(document).on('click', '.select', function() {
        if(player_count >= max_players) {
            alert('You already have 11 players!')
            return;
        }
        player_count++;
        players_chosen.push($(this).attr('data-id'));
        console.log(`old_score : ${score}`);
        score = score - $(this).attr('score');
        console.log(`new_score : ${score}`);
        $('#score').text(score); 
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
        console.log(`old_score : ${score}`);
        score = +score + +$(`#${$(this).attr('id')}`).attr('score');
        console.log(`new_score : ${score}`);
        $('#score').text(score); 
        $(this).remove();
    });

    // Submit players
    $(document).on('click', '#submit-button', function() {
        if(player_count != 11) {
            alert("You should choose 11 players!");
            return;
        }
        console.log('Submit my team!');
        var myteam = {
            match_id: match_id,
            player_count: player_count,
            players: JSON.stringify(players_chosen),
            score: JSON.stringify(score)
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