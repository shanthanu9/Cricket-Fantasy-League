$(document).ready(function() {
    var $matches = $('#matches');
    var $live_match = $('.live_match');
    var $batting = $('.batting');
    var $bowling = $('.bowling');
    var $batting_table = $('.batting_table');
    var $batting_score = $('.batting_score');
    var $bowling_table = $('.bowling_table');
    var $selected_players = $('.selected_players');

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
            if(match.status != 'Result') {
                if(match.status == 'default') match.status = 'Scheduled';
                $matches.append(
                    `<div class="match card">`+
                        `<p>${match.status}<\p>`+
                        `<p>${match.teams[0].name} : ${match.teams[0].score}</p>`+
                        `<p>${match.teams[1].name} : ${match.teams[1].score}</p>`+
                        `<button match_id="${match.id}" class="make_team">Make team!</button>`+
                    `</div>`
                    );
            }
            else {
                $matches.append(
                    `<div class="match card">`+
                        `<p>${match.status}<\p>`+
                        `<p>${match.teams[0].name} : ${match.teams[0].score}</p>`+
                        `<p>${match.teams[1].name} : ${match.teams[1].score}</p>`+
                        `<button match_id="${match.id}" class="make_team" disabled>Match done!</button>`+
                    `</div>`
                    );
            }
        }
        // slick carousal
        $matches.slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 3
        });
    });

    socket.on('live_match', function(msg) {
        console.log(msg.match);
        $batting_table.empty();
        $batting_score.empty();
        $bowling_table.empty();
        $selected_players.empty();

            
            if(msg.match['matchcards'][0].headline === "Batting"){
                $batting_score.append(
                    `<div class="card1">`+
                    `<p>Batting Team: ${msg.match['matchcards'][0].teamName}</p>`+
                    `<p>Score : ${msg.match['matchcards'][0].total}</p>`+
                    `<p>Runs : ${msg.match['matchcards'][0].runs}</p>`+
                    `</div>`
                
                );
                // $batting.append(`<table class="batting_table"></table>`);
                    $batting_table.append(`<tr><th>P.Name</th><th>Runs</th><th>Balls Faced</th></tr>`);
                    for(var i=0;i<msg.match['matchcards'][0].playerDetails.length;i++){
                        if(msg.match['matchcards'][0].playerDetails[i].dismissal === "not out"){
                            $batting_table.append(
                                `<tr>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].playerName} <sup>*</sup></td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].runs}</td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].ballsFaced}</td>`+ 
                                `</tr>`
                            );
                        }
                        else{
                            $batting_table.append(
                                `<tr>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].playerName}</td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].runs}</td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].ballsFaced}</td>`+ 
                                `</tr>`
                            );
                        }
                    }    
            }

            

            else if(msg.match['matchcards'][1].headline === "Batting"){
                $batting_score.append(
                    `<p>Batting Team: ${msg.match['matchcards'][1].teamName}</p>`+
                    `<p>Score : ${msg.match['matchcards'][1].total}</p>`+
                    `<p>Runs : ${msg.match['matchcards'][1].runs}</p>`
                );
                // $batting.append(`<table class="batting_table"></table>`);
                    $batting_table.append(`<tr><th>P.Name</th><th>Runs</th><th>Balls Faced</th></tr>`);

                    for(var i=0;i<msg.match['matchcards'][1].playerDetails.length;i++){
                        if(msg.match['matchcards'][1].playerDetails[i].dismissal === "not out"){
                            $batting_table.append(
                                `<tr>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].playerName} <sup>*</sup></td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].runs}</td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].ballsFaced}</td>`+ 
                                `</tr>`
                            );
                        }
                        else{
                            $batting_table.append(
                                `<tr>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].playerName}</td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].runs}</td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].ballsFaced}</td>`+ 
                                `</tr>`
                            );
                        }
                    }
            }


            if(msg.match['matchcards'][0].headline === "Bowling"){
                $bowling_table.append(
                    // `<p>Bowling Team: ${msg.match['matchcards'][0].teamName}</p>`
                    // `<p>Score : ${msg.match['matchcards'][0].total}</p>`+
                    // `<p>Runs : ${msg.match['matchcards'][0].runs}</p>`
                    `<tr><th>P.Name</th><th>Runs</th><th>Overs</th><th>Wickets</th><th>Economy</th></tr>`

                );
                    for(var i=0;i<msg.match['matchcards'][0].playerDetails.length;i++){
                            $bowling_table.append(
                                `<tr>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].playerName}</td>`+ 
                                `<td>${msg.match['matchcards'][0].playerDetails[i].conceded}</td>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].overs}</td>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].wickets}</td>`+
                                `<td>${msg.match['matchcards'][0].playerDetails[i].economyRate}</td>`+ 
                                `</tr>`
                            );
                    }    
            }
            
            if(msg.match['matchcards'][1].headline === "Bowling"){
                $bowling_table.append(
                    // `<p>Bowling Team: ${msg.match['matchcards'][1].teamName}</p>`
                    // `<p>Score : ${msg.match['matchcards'][0].total}</p>`+
                    // `<p>Runs : ${msg.match['matchcards'][0].runs}</p>`+
                    `<tr><th>P.Name</th><th>Runs</th><th>Overs</th><th>Wickets</th><th>Economy</th></tr>`
                );
                    for(var i=0;i<msg.match['matchcards'][1].playerDetails.length;i++){
                            $bowling_table.append(
                                `<tr>`+
                                `<td>${msg.match['matchcards'][1].playerDetails[i].playerName}</td>`+ 
                                `<td>${msg.match['matchcards'][1].playerDetails[i].conceded}</td>`+
                                `<td>${msg.match['matchcards'][1].playerDetails[i].overs}</td>`+
                                `<td>${msg.match['matchcards'][1].playerDetails[i].wickets}</td>`+
                                `<td>${msg.match['matchcards'][1].playerDetails[i].economyRate}</td>`+ 
                                `</tr>`
                            );
                    }    
            }
            

            $selected_players.append(
                `<tr><th>${msg.match['scores'][0].teamname}</th><th>Points</th><th>${msg.match['scores'][1].teamname}</th><th>Points</th></tr>`
            );

            for(var i=0; i<msg.match['scores'][0].roster.length ; i++ ){
                $selected_players.append(
                    `<tr>`+
                    `<td>${msg.match['scores'][0].roster[i].player}</td>`+ 
                    `<td>${msg.match['scores'][0].roster[i].score}</td>`+                     
                    `<td>${msg.match['scores'][1].roster[i].player}</td>`+                                         
                    `<td>${msg.match['scores'][1].roster[i].score}</td>`+ 
                    `</tr>`
                );
            }

    });

    // AJAX request for creating a team
    $(document).on('click', '.make_team', function() { // This syntax because event listener is being added to dynamically created nodes
        if($matches.attr('match_id')) {
            alert('You can play one match at a time!');
            return;
        }
        var match_id = $(this).attr('match_id');
        // Redirect to relevant URL
        window.location.href = `/myteam?match_id=${match_id}`;
    });
});