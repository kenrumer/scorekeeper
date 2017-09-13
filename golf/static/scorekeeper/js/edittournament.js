/* global $, courseTees, courses, tournamentName, dateStart, numRounds, players */
  var editTournamentTable;
  var newTournamentTable;
  var addRowId = 0;
  var slope = 86;

  function updateScorecardRow(data) {
    var rowId = data.getAttribute('data-rowId');
    var playerHCP = $('#hcp'+rowId).val();
    var holes = $('[name="holeout'+rowId+'"]');
    var totalout = 0;
    holes.each(function(i, item) {
      totalout += parseInt($(item).val());
    })
    $('#totalout'+rowId).val(totalout);
    holes = $('[name="holein'+rowId+'"]');
    var totalin = 0;
    holes.each(function(i, item) {
      totalin += parseInt($(item).val());
    });
    $('#totalin'+rowId).val(totalin);
    $('#total'+rowId).val(totalin+totalout);
    $('#totalnet'+rowId).val(totalin+totalout-playerHCP);
  }

  function playerChange(data) {
    var rowId = data.getAttribute('data-rowId');
    var hcpInput = document.getElementById('hcp'+rowId);
    var selValue = data.options[data.selectedIndex].value;
    var id = selValue.split('|')[0];
    var hcp = selValue.split('|')[1];
    if (hcp) {
      hcpInput.value = Math.round(hcp * slope / 113);
    } else {
      hcpInput.value = 0;
    }
    updateScorecardRow(hcpInput);
  }

  function editScorecard(scorecard_id) {
    addRowId = 0;
    $('#addRowToScorecard').css('display', 'block');
    if (courses.length > 1) {
      $('#enterScorecardCourse').modal({backdrop: 'static', keyboard: false}, event.target).show();
    } else {
      $('#scorecard >tbody').html('');
      addRowToScorecard(player_id);
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    }
  }

  function editScorecardRow(player_id) {
    addRowId = 0;
    if (!courses.length > 1) {
      $('#enterScorecardCourse').modal({backdrop: 'static', keyboard: false}, event.target).show();
    } else {
      $('#scorecard >tbody').html('');
      addRowToScorecard(player_id);
      $('#addRowToScorecard').css('display', 'none');
      $('#scorecardRowButton0').css('display', 'none');
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    }
  }

  function addRowToScorecard() {
    var teeList = '';
    var playerList = '';
    for (var i = 0; i < players.length; i++) {
      playerList += '<option value='+players[i].fields.club_member_number+'|'+players[i].fields.handicap_index+'>'+players[i].fields.name+'</option>';
    }
    if (courseTees.length == 1) {
      teeList = ' \
        <div style="background-color:'+courseTees[0].color_text+'">&nbsp;</div>';
    } else {
      teeList = ' \
        <div class="dropdown"> \
          <button id="teeSelectButton'+addRowId+'" class="dropdown-toggle" style="background-color:'+courseTees[0].color_text+'" type="button" data-toggle="dropdown" aria-expanded="true"> \
            <span class="caret"></span> \
          </button> \
          <ul id="courseTees'+addRowId+'" class="dropdown-menu" aria-labelledby="dropdownMenu1">';
      $.each(courseTees, function(i, item) {
        teeList += '<li style="background-color:'+item.color_text+'"><a href="#" onclick="javascript:teeChange('+addRowId+', "'+item.color_text+'", '+item.slope+')">'+item.short_color_text+'</a>';
      })
      teeList += ' \
          </ul> \
        </div>';
    }
    console.log(courseTees);
    $('#scorecard > tbody').append(' \
      <tr id="scorecardRow'+addRowId+'" data-rowId="'+addRowId+'"> \
        <td> \
          <button class="plusMinusButton" id="removeRowFromScorecard" data-rowId="'+addRowId+'">-</button> \
        </td> \
        <td> \
          <select name="playerNames" id="playerNames'+addRowId+'" style="width: 140px" data-rowId="'+addRowId+'" onchange="javascript:playerChange(this);"> \
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
    $('#playerNames'+addRowId).focus();
    addRowId++;
  }
  
  function setScorecardCourseAndCourseTee() {
    $('#enterScorecardCourse').modal('hide');
    $('#scorecard >tbody').html('');
    addRowToScorecard();
    $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
  }

  function teeChange(rowId, color, newSlope) {
    $('#hcp'+rowId).val(Math.round($('playerNames'+rowId).val().split('|')[1] * newSlope / 113));
    $('#teeSelectButton'+rowId).css('background-color', color);
  }

  $(document).ready(function() {

    //Scorecard actions
    $('#scorecard').on('input', '#scorecardCell', function(event) {
      updateScorecardRow(this);
    });
    $('#scorecard').on('click', '#removeRowFromScorecard', function() {
      var rowId = this.getAttribute('data-rowId');
      $('#scorecardRow'+rowId).html('');
    });
    $('#enterScorecardButton').click(function() {
      console.log($('#scorecard'));
    });
    $('#addRowToScorecard').click(function(event) {
      addRowToScorecard();
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
            console.log(courses.length);
            if (courses.length > 1) {
              $('#enterScorecardCourse').modal({backdrop: 'static', keyboard: false}, event.target).show();
            } else {setScorecardCourseAndCourseTee
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