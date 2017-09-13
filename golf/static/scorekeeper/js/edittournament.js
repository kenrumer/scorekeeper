/* global $, courseTees, courses, tournamentName, dateStart, numRounds, players, tournamentId */
  var editTournamentTable;
  var newTournamentTable;
  var addRowId = 0;

  function updateScorecardRow(data) {
    var rowId = $(data).attr('data-rowId');
    var playerHCP = $('#hcp'+rowId).val();
    var holes = $('[name="holeout'+rowId+'"]');
    var totalout = 0;
    holes.each(function(i, item) {
      totalout += parseInt($(item).val(), 10);
    });
    $('#totalout'+rowId).val(totalout);
    holes = $('[name="holein'+rowId+'"]');
    var totalin = 0;
    holes.each(function(i, item) {
      totalin += parseInt($(item).val(), 10);
    });
    $('#totalin'+rowId).val(totalin);
    $('#total'+rowId).val(totalin+totalout);
    $('#totalnet'+rowId).val(totalin+totalout-playerHCP);
  }

  function editScorecard(scorecard_id) {
    console.log("test3");
    /*addRowId = 0;
    $('#addRowToScorecard').css('display', 'block');
    if (courses.length > 1) {
      $('#enterScorecardCourse').modal({backdrop: 'static', keyboard: false}, event.target).show();
    } else {
      $('#scorecard >tbody').html('');
      addRowToScorecard();
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    }*/
  }

  function editScorecardRow(player_id) {
    console.log("test4");
    /*addRowId = 0;
    if (!courses.length > 1) {
      $('#enterScorecardCourse').modal({backdrop: 'static', keyboard: false}, event.target).show();
    } else {
      $('#scorecard >tbody').html('');
      addRowToScorecard();
      $('#addRowToScorecard').css('display', 'none');
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    }*/
  }

  function addRowToScorecard() {
    var teeList = "";
    var playerList = "";
    for (var i = 0; i < players.length; i++) {
      playerList += '<option value='+players[i].fields.club_member_number+'|'+players[i].fields.handicap_index+'>'+players[i].fields.name+'</option>';
    }
    if (courseTees.length == 1) {
      teeList = '<div id="playerTee'+addRowId+'" data-slope="'+courseTees[0].slope+'" data-color="'+courseTees[0].color_text+'" style="background-color:'+courseTees[0].color_text+'">&nbsp;</div>';
    } else {
      teeList = '<div id="playerTee'+addRowId+'" data-slope="'+courseTees[0].slope+'" data-color="'+courseTees[0].color_text+'" data-id="'+courseTees[0].id+'" class="dropdown"> \
          <button id="teeSelectButton'+addRowId+'" class="dropdown-toggle" style="background-color:'+courseTees[0].color_text+'" type="button" data-toggle="dropdown" aria-expanded="true"> \
            <span class="caret"></span></button> \
          <ul id="courseTees'+addRowId+'" class="dropdown-menu" aria-labelledby="teeSelectButton'+addRowId+'">';
      $.each(courseTees, function(i, item) {
        teeList += '<li style="background-color:'+item.color_text+'"><a href="#" id="teeChangeButton" data-rowId="'+addRowId+'" data-slope="'+item.slope+'" data-color="'+item.color_text+'" data-id="'+item.id+'">'+item.color_text+'</a></li>';
      });
      teeList += '</ul></div>';
    }
    $('#scorecard >tbody').append(' \
      <tr id="scorecardRow'+addRowId+'" data-rowId="'+addRowId+'" data-currentSlope='+courseTees[0].slope+'> \
        <td> \
          <button class="plusMinusButton" id="removeRowFromScorecard" data-rowId="'+addRowId+'">-</button> \
        </td> \
        <td> \
          <select id="playerNamesSelect" style="width: 140px" data-rowId="'+addRowId+'"> \
            <option>----------------------------</option>'+playerList+'</select> \
        </td><td>'+teeList+'</td><td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[0].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[1].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[2].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[3].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[4].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[5].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[6].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[7].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holeout'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[8].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" id="totalout'+addRowId+'" value="'+courseTees[0].parOut+'" disabled> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[9].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[10].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[11].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[12].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[13].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[14].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[15].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[16].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" name="holein'+addRowId+'" type=number min=1 max=99 value='+courseTees[0].tees[17].par+'> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" id="totalin'+addRowId+'" value="'+courseTees[0].parIn+'" disabled> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" id="total'+addRowId+'" value="'+courseTees[0].parTotal+'" disabled> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" id="hcp'+addRowId+'" value=0 disabled> \
        </td> \
        <td> \
          <input class="scorecardCell" data-rowId="'+addRowId+'" id="totalnet'+addRowId+'" value="'+courseTees[0].parTotal+'" disabled> \
        </td> \
      </tr>');
    $('#scorecardRow'+addRowId+' #playerNamesSelect').focus();
    addRowId++;
  }

  $(document).ready(function() {

    //Select course actions
    $('#enterScorecardCourseButton').click(function(event) {
      $('#enterScorecardCourse').modal('hide');
      $('#scorecard >tbody').html('');
      addRowToScorecard();
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    //Scorecard actions
    $('#scorecard').on('input', '#scorecardCell', function(event) {
      updateScorecardRow(this);
    });
    $('#scorecard').on('click', '#removeRowFromScorecard', function() {
      var rowId = $(this).attr('data-rowId');
      $('#scorecardRow'+rowId).html('');
    });
    $('#addRowToScorecard').click(function(event) {
      addRowToScorecard();
    });
    $('#scorecard').on('change', '#playerNamesSelect', function(event) {
      var rowId = $(this).attr('data-rowId');
      var hcp = $(this).val().split('|')[1];
      if (hcp) {
        $('#hcp'+rowId).val(Math.round(hcp * parseInt($('#scorecardRow'+rowId).attr('data-currentSlope'), 10) / 113));
      } else {
        $('#hcp'+rowId).val(0);
      }
      updateScorecardRow(this);
    });
    $('#scorecard').on('click', '#teeChangeButton', function(event) {
      var rowId = $(this).attr('data-rowId');
      var newSlope = $(this).attr('data-slope');
      var color = $(this).attr('data-color');
      $('#scorecardRow'+rowId).attr('data-currentSlope', newSlope);
      $('#hcp'+rowId).val(Math.round($('#scorecardRow'+rowId+' #playerNamesSelect').val().split('|')[1] * newSlope / 113));
      $('#teeSelectButton'+rowId).css('background-color', color);
      $('#playerTee'+rowId).attr('data-slope', newSlope);
      $('#playerTee'+rowId).attr('data-color', color);
      $('#playerTee'+rowId).attr('data-id', $(this).attr('data-id'));
      updateScorecardRow(this);
    });
    //This is when we store data in the db
    $('#enterScorecardButton').click(function(event) {
      var scores = [];
      $('#scorecard #playerNamesSelect').each(function() {
        var score = {};
        var clubMemberNumber = $(this).val().split('|')[0];
        var playerName = $('option:selected',this).text();
        var hcpIndex = $(this).val().split('|')[1];
        var rowId = $(this).attr('data-rowId');
        var slope = parseInt($('#playerTee'+rowId).attr('data-slope'), 10);
        var teeColor = $('#playerTee'+rowId).attr('data-color');
        var teeId = parseInt($('#playerTee'+rowId).attr('data-id'), 10);
        var courseHCP = parseInt($('#hcp'+rowId).val(), 10);
        score.clubMemberNumber = clubMemberNumber;
        score.playerName = playerName;
        score.hcpIndex = hcpIndex;
        score.slope = slope;
        score.teeColor = teeColor;
        score.teeId = teeId;
        score.courseHCP = courseHCP;
        
        var holes = $('[name="holeout'+rowId+'"]');
        var totalout = 0;
        holes.each(function(i, item) {
          var holeNumber = i;
          score['hole'+holeNumber] = parseInt($(item).val(), 10);
          totalout += parseInt($(item).val(), 10);
        });
        score.totalout = totalout;
        $('#totalout'+rowId).val(totalout);
        holes = $('[name="holein'+rowId+'"]');
        var totalin = 0;
        holes.each(function(i, item) {
          var holeNumber = i+9;
          score['hole'+holeNumber] = parseInt($(item).val(), 10);
          totalin += parseInt($(item).val(), 10);
        });
        score.totalin = totalin;
        score.total = totalin+totalout;
        score.totalnet = totalin+totalout-courseHCP;
        $('#totalin'+rowId).val(totalin);
        $('#total'+rowId).val(totalin+totalout);
        $('#totalnet'+rowId).val(totalin+totalout-courseHCP);
        console.log(score);
        scores.push(score);
      });
      var tournamentData;
      if (!newTournamentTable.data().count()) {
        tournamentData = [];
      } else {
        tournamentData = newTournamentTable.rows().data();
      }
      var context = {
        tournamentId: tournamentId,
        tournamentData: tournamentData,
        courseTees: courseTees,
        scores: scores
      };
      console.log(context);
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      $.post('/golf/calculatescores/', context).done(function(data) {
        $('#loadingDialog').modal('hide');
      }).fail(function(xhr, textStatus, error) {
        $('#loadingDialog').modal('hide');
        alert('failed to store scorecard: '+xhr.responseText);
        console.log('failed to load players!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });
    });

    //New tournament table
    newTournamentTable = $('#newTournamentTable').DataTable( {
      'dom': 'Bfrtip',
      'buttons': [
        {
          'text': '<u>A</u>dd Score Card',
          'key': {
            'key': 'a',
            'shiftKey': true
          },
          'action': function ( event, dt, node, config ) {
            event.stopPropagation();
            addRowId = 0;
            if (courses.length > 1) {
              $('#enterScorecardCourse').modal({backdrop: 'static', keyboard: false}, event.target).show();
            } else {
              $('#scorecard >tbody').html('');
              addRowToScorecard();
              $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
            }
          }
        }
      ],
      'scrollY': '65vh',
      'scrollCollapse': false,
      'paging': false,
      'processing': true,
      'language': {
        'processing': '<p class="bg-warning">Processing...</p>'
      }
    });

    //Edit tournament table
    editTournamentTable = $('#editTournamentTable').DataTable( {
      'dom': 'Bfrtip',
      'buttons': [
        {
          'text': '<u>A</u>dd Score Card',
          'key': {
            'key': 'a',
            'shiftKey': true
          },
          'action': function ( event, dt, node, config ) {
            event.stopPropagation();
            addRowId = 0;
            if (courses.length > 1) {
              $('#enterScorecardCourse').modal({backdrop: 'static', keyboard: false}, event.target).show();
            } else {
              $('#scorecard >tbody').html('');
              addRowToScorecard();
              $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
            }
          }
        }
      ],
      'scrollY': '65vh',
      'scrollCollapse': false,
      'paging': false,
      'processing': true,
      'language': {
        'processing': '<p class="bg-warning">Processing...</p>'
      }
    });
  });