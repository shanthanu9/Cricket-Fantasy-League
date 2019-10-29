$(document).ready(function() {
    // TODO: Replace with player details fetched from URL
    var teams = [[], []];
    for(var i = 0; i < 11; i++) {
        teams[0].push(`a${i}`);
        teams[1].push(`b${i}`);
    }

    // Append buttons to div tag
    var i = 0;
    for(var team of teams) {
        var player_id = 0;
        for(player of team) {
            $('#teams').append(
                `<button class="select" id="team-${i}-player-${player_id}">${player}</button>`
            );
            player_id++;
        }
        i++;
    } 

    // Selecting players
    $(document).on('click', '.select', function() {
        $('#chosen').append(
            `<button class="deselect" id="${$(this).attr('id')}">${$(this).text()}</button>`
        );
        $(this).attr('disabled', true);
    });

    // Removing players
    $(document).on('click', '.deselect', function() {
        $(`#${$(this).attr('id')}`).attr('disabled', false);
        $(this).remove();
    });
});