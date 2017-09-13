/* global $, courseTees, courses, tournamentName, dateStart, numRounds, players */
  var editTournamentTable;
  var newTournamentTable;
  var addRowId = 0;

  function updateScorecardRow(data) {
    console.log("test1");
    var rowId = data.getAttribute('data-rowId');
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
    console.log("test5");
    var teeList = "";
    var playerList = "";
    for (var i = 0; i < players.length; i++) {
      playerList += '<option value='+players[i].fields.club_member_number+'|'+players[i].fields.handicap_index+'>'+players[i].fields.name+'</option>';
    }
    if (courseTees.length == 1) {
      teeList = "<div style='background-color:"+courseTees[0].color_text+"'>&nbsp;</div>";
    } else {
      teeList = "<div class='dropdown'> \
          <button id='teeSelectButton"+addRowId+"' class='dropdown-toggle' style='background-color:"+courseTees[0].color_text+"' type='button' data-toggle='dropdown' aria-expanded='true'> \
            <span class='caret'></span></button> \
          <ul id='courseTees"+addRowId+"' class='dropdown-menu' aria-labelledby='teeSelectButton"+addRowId+"'>";
      $.each(courseTees, function(i, item) {
        teeList += "<li style='background-color:"+item.color_text+"'><a href='#'>"+item.color_text+"</a></li>";
      });
      teeList += "</ul></div>";
    }
    console.log(teeList);
    $('#scorecard >tbody').append(' \
      <tr id="scorecardRow'+addRowId+'" data-rowId="'+addRowId+'" data-currentSlope='+courseTees[0].slope+'> \
        <td> \
          <button class="plusMinusButton" id="removeRowFromScorecard" data-rowId="'+addRowId+'">-</button> \
        </td> \
        <td> \
          <select name="playerNames" id="playerNames" style="width: 140px" data-rowId="'+addRowId+'"> \
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
    $('#playerNames').focus();
    addRowId++;
  }

  function teeChange(rowId, color, newSlope) {
    console.log("test6");
    console.log($('#playerNames').val());
    $('#scorecardRow'+rowId).attr('data-currentSlope', newSlope);
    $('#hcp'+rowId).val(Math.round($('#playerNames').val().split('|')[1] * newSlope / 113));
    $('#teeSelectButton'+rowId).css('background-color', color);
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
    $('#scorecard').on('change', '#playerNames', function(event) {
      var rowId = $(this).attr('data-rowId');
      var hcp = $(this).val().split('|')[1];
      if (hcp) {
        $('#hcp'+rowId).val(Math.round(hcp * parseInt($('#scorecardRow'+rowId).attr('data-currentSlope'), 10) / 113));
      } else {
        $('#hcp'+rowId).val(0);
      }
      updateScorecardRow(this);
    });
    $('#scorecard').on('click', '.dropdown-toggle li > a', function(event) {
      console.log(this);
    })

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