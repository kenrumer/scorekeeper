/* global $, courseTeesJSON, coursesJSON, tournamentName, dateStart, numRounds, playersJSON, id, name, duplicate, dateId, date, dateDuplicate */
  var editTournamentTable;
  var newTournamentTable;
  var addRowId = 0;

  function updateScorecardRound(data) {
    var rowId = $(data).attr('data-rowId');
    var playerHCP = $('#hcp'+rowId).val();
    var holesOut = $('[data-holeOut="'+rowId+'"]');
    var totalOut = 0;
    holesOut.each(function(i, item) {
      totalOut += parseInt($(item).val(), 10);
    });
    var holesIn = $('[data-holeIn="'+rowId+'"]');
    var totalIn = 0;
    holesIn.each(function(i, item) {
      totalIn += parseInt($(item).val(), 10);
    });
    $('#totalIn'+rowId).val(totalIn);
    $('#total'+rowId).val(totalIn+totalOut);
    $('#totalNet'+rowId).val(totalIn+totalOut-playerHCP);
  }

  function editScorecard(scorecardId) {
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

  function editScorecardRow(playerId) {
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
  
  function playerList() {
    var playerList = "";
    $.each(playersJSON, function(i, item) {
      playerList += '<option value='+item.club_member_number+' data-handicapIndex='+item.handicap_index+' data-clubMemberNumber='+item.club_member_number+'>'+item.name+'</option>';
    });
    return playerList;
  }
  
  function teeList() {
    var teeList = "";
    if (courseTeesJSON.length == 0) {
      return "";
    }
    if (courseTeesJSON.length == 1) {
      teeList = '<div id="playerTee'+addRowId+'" data-courseTeeSlope="'+courseTeesJSON[0].slope+'" data-courseTeeColor="'+courseTeesJSON[0].color+'" data-courseTeeId="'+courseTeesJSON[0].id+'" style="background-color:'+courseTeesJSON[0].color+'">'+courseTeesJSON[0].color+'</div>';
    } else {
      teeList = '<div id="playerTee'+addRowId+'" data-courseTeeSlope="'+courseTeesJSON[0].slope+'" data-courseTeeColor="'+courseTeesJSON[0].color+'" data-courseTeeId="'+courseTeesJSON[0].id+'" class="dropdown">';
      teeList += '  <button id="teeSelectButton'+addRowId+'" class="dropdown-toggle" style="background-color:'+courseTeesJSON[0].color+'" type="button" data-toggle="dropdown" aria-expanded="true"><span class="caret"></span></button>';
      teeList += '  <ul id="courseTees'+addRowId+'" class="dropdown-menu" aria-labelledby="teeSelectButton'+addRowId+'">';
      $.each(courseTeesJSON, function(i, item) {
        teeList += '    <li style="background-color:'+item.color+'"><a href="#" id="courseTeeChangeButton" data-rowId="'+addRowId+'" data-courseTeeSlope="'+item.slope+'" data-courseTeeColor="'+item.color+'" data-courseTeeId="'+item.id+'">'+item.color+'</a></li>';
      });
      teeList += '  </ul></div>';
    }
    return teeList;
  }

  function addRowToScorecard() {
    var appendText = '<tr id="scorecardRow'+addRowId+'" data-rowId="'+addRowId+'" data-slope='+courseTeesJSON[0].slope+'>';
    appendText += '<td><button class="plusMinusButton" id="removeRowFromScorecard" data-rowId="'+addRowId+'">-</button></td>';
    appendText += '<td><select id="playerNamesSelect" style="width: 140px" data-rowId="'+addRowId+'"><option>----------------------------</option>'+playerList()+'</select></td><td>'+teeList()+'</td>';
    for (var i = 1; i < 10; i++) {
      appendText += '<td><input class="scorecardCell" data-rowId="'+addRowId+'" data-holeOut="'+addRowId+'" type=number min=1 max=99 value='+courseTeesJSON[0].tees[i-1].par+'></td>';
    }
    appendText += '<td><input class="scorecardCell" data-rowId="'+addRowId+'" id="totalOut'+addRowId+'" value="'+courseTeesJSON[0].parOut+'" disabled></td>';
    for (var i = 9; i < 18; i++) {
      appendText += '<td><input class="scorecardCell" data-rowId="'+addRowId+'" data-holeIn="'+addRowId+'" type=number min=1 max=99 value='+courseTeesJSON[0].tees[i-1].par+'></td>';
    }
    appendText += '<td><input class="scorecardCell" data-rowId="'+addRowId+'" id="totalIn'+addRowId+'" value="'+courseTeesJSON[0].parIn+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-rowId="'+addRowId+'" id="total'+addRowId+'" value="'+courseTeesJSON[0].parTotal+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-rowId="'+addRowId+'" id="hcp'+addRowId+'" value="0" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-rowId="'+addRowId+'" id="totalNet'+addRowId+'" value="'+courseTeesJSON[0].parTotal+'" disabled></td></tr>';
    $('#scorecard >tbody').append(appendText);
    $('#scorecard #scorecardRow'+addRowId+' #playerNamesSelect').focus();
    addRowId++;
  }

  $(document).ready(function() {

    //Load the courses list for select course modal
    $.each(coursesJSON, function (i, item) {
      var option = '<option value="'+item.id+'">'+item.name+'</option>';
      $('#enterScorecardCourse').append(option);
    });
    //Load the courseTees for the score card
    $.each(courseTeesJSON, function(i, item) {
      var row = '<tr style="background-color:'+item.color+'">';
      row += '  <th></th>';
      row += '  <th></th>';
      row += '  <th>'+item.color+'</th>';
      for (var i = 0; i < 9; i++) {
        row += '  <th><input class="scorecardCell" value="'+item.tees.i.yardage+'" disabled></th>';
      }
      row += '  <th><input class="scorecardCell" value="'+item.yardageIn+'" disabled></th>';
      for (var i = 10; i < 18; i++) {
        row += '  <th><input class="scorecardCell" value="'+item.tees.i.yardage+'" disabled></th>';
      }
      row += '  <th><input class="scorecardCell" value="'+item.yardageOut+'" disabled></th>';
      row += '  <th><input class="scorecardCell" value="'+item.yardageTotal+'" disabled></th>';
      row += '  <th></th>';
      row += '  <th></th>';
      row += '</tr>';
      row += '<tr style="background-color:'+item.color+'">';
      row += '  <th></th>';
      row += '  <th></th>';
      row += '  <th>Par</th>';
      for (var i = 0; i < 9; i++) {
        row += '  <th><input class="scorecardCell" value="'+item.tees.i.par+'" disabled></th>';
      }
      row += '  <th><input class="scorecardCell" value="'+item.parIn+'" disabled></th>';
      for (var i = 10; i < 18; i++) {
        row += '  <th><input class="scorecardCell" value="'+item.tees.i.par+'" disabled></th>';
      }
      row += '  <th><input class="scorecardCell" value="'+item.parOut+'" disabled></th>';
      row += '  <th><input class="scorecardCell" value="'+item.parTotal+'" disabled></th>';
      row += '  <th></th>';
      row += '  <th></th>';
      row += '</tr>';
      $("#scorecard thead").append(row);
    });
    //Load the players for the score card scorer, attest
    $.each(playersJSON, function(i, item) {
      var option = '<option data-value="'+item.club_member_number+'">'+item.name+'</option>';
      $('#scorecardScorer').append(option);
      $('#scorecardAttest').append(option);
    });

    //Select course actions
    $('#enterScorecardCourseButton').click(function(event) {
      $('#enterScorecardCourse').modal('hide');
      $('#scorecard >tbody').html('');
      addRowToScorecard();
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    //Scorecard actions
    $('#scorecard').on('input', '#scorecardCell', function(event) {
      updateScorecardRound(this);
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
        $('#hcp'+rowId).val(Math.round(hcp * parseInt($('#scorecardRow'+rowId).attr('data-slope'), 10) / 113));
      } else {
        $('#hcp'+rowId).val(0);
      }
      updateScorecardRound(this);
    });
    $('#scorecard').on('click', '#courseTeeChangeButton', function(event) {
      var rowId = $(this).attr('data-rowId');
      var newSlope = $(this).attr('data-slope');
      var color = $(this).attr('data-color');
      $('#scorecardRow'+rowId).attr('data-slope', newSlope);
      $('#hcp'+rowId).val(Math.round($('#scorecardRow'+rowId+' #playerNamesSelect').val().split('|')[1] * newSlope / 113));
      $('#teeSelectButton'+rowId).css('background-color', color);
      $('#playerTee'+rowId).attr('data-slope', newSlope);
      $('#playerTee'+rowId).attr('data-color', color);
      $('#playerTee'+rowId).attr('data-courseTeeId', $(this).attr('dataCourseTeeId'));
      updateScorecardRound(this);
    });
    //This is when we store data in the db.
    //Creates a scorecard, first, then throws the rest to the plugin.
    //Doing all of this in 1 post to save time/effort
    $('#enterScorecardButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var scores = [];
      $('#scorecard #playerNamesSelect').each(function() {
        var score = {};
        var playerName = $('option:selected',this).text();
        var clubMemberNumber = $('option:selected',this).attr('data-clubMemberNumber');
        var handicapIndex = $('option:selected',this).attr('data-handicapIndex');
        var selectValue = $('option:selected',this).val();
        console.log(playerName);
        console.log(clubMemberNumber);
        console.log(handicapIndex);
        console.log(selectValue);
        var rowId = $(this).attr('data-rowId');
        var courseTeeId = parseInt($('#playerTee'+rowId).attr('data-courseTeeId'), 10);
        var courseHCP = parseInt($('#hcp'+rowId).val(), 10);
        score.clubMemberNumber = clubMemberNumber;
        score.playerName = playerName;
        score.handicapIndex = handicapIndex;
        score.courseTeeId = courseTeeId;
        score.courseHCP = courseHCP;
        
        var holesOut = $('[data-holeOut="'+rowId+'"]');
        var totalout = 0;
        holesOut.each(function(i, item) {
          var holeNumber = i;
          score['hole'+holeNumber] = parseInt($(item).val(), 10);
          totalout += parseInt($(item).val(), 10);
        });
        score.totalout = totalout;
        $('#totalout'+rowId).val(totalout);
        //holes = $('[name="holein'+rowId+'"]');
        var holesIn = $('[data-holeIn="'+rowId+'"]');
        var totalin = 0;
        holesIn.each(function(i, item) {
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
      console.log($('#newScorecardScorer'));
      var context = {
        teeTime: $('#newScorecardStartTime').val(),
        finishTime: $('#newScorecardFinishTime').val(),
        scorer: $('#newScorecardScorer').val(),
        scorerId:$('#newScorecardScorer').data('value'),
        attest: $('#newScorecardAttest').val(),
        attestId:$('#newScorecardAttest').data('value'),
        tournamentId: id,
        date: date,
        scores: JSON.stringify(scores)
      };
      console.log(context);
      /*$.post('/golf/calculatescores/', context).done(function(data) {
        $('#loadingDialog').modal('hide');
      }).fail(function(xhr, textStatus, error) {
        $('#loadingDialog').modal('hide');
        $('#errorDialog').modal({}).show();
        $('#errorHeader').text('failed to store scorecard');
        $('#errorText').text(xhr.responseText);
        console.log('failed to load players!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });*/
      $('#loadingDialog').modal('hide');
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
            if (coursesJSON.length > 1) {
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
            if (coursesJSON.length > 1) {
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
    $('#newScorecardStartTimePicker').datetimepicker({format: 'LT'});
    $('#newScorecardFinishTimePicker').datetimepicker({format: 'LT', "defaultDate":new Date()});
    $('#editTournamentTimeStartDatePicker').datetimepicker({format: 'LT'});
    $('#editTournamentTimeEndDatePicker').datetimepicker({format: 'LT'});
  });