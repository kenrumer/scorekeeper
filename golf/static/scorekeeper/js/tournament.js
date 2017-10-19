/* global $, tournamentId, tournamentName, numRounds, tournamentRoundsJSON, playersJSON, availableCoursesJSON, availableCourseTeesJSON, roundId, moment */
  var newTournamentTable;
  var addRowId = 0;

  function updateScorecardRound(data) {
    var rowId = $(data).data('rowId');
    var playerHCP = $('#hcp'+rowId).val();
    var holesOut = $('[data-hole-out="'+rowId+'"]');
    var totalOut = 0;
    holesOut.each(function(i, item) {
      totalOut += parseInt($(item).val(), 10);
    });
    var holesIn = $('[data-hole-in="'+rowId+'"]');
    var totalIn = 0;
    holesIn.each(function(i, item) {
      totalIn += parseInt($(item).val(), 10);
    });
    $('#totalIn'+rowId).val(totalIn);
    $('#total'+rowId).val(totalIn+totalOut);
    $('#totalNet'+rowId).val(totalIn+totalOut-playerHCP);
  }

  function editScorecard(scorecardId) {
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
      playerList += '<option value='+item.club_member_number+' data-handicap-index='+item.handicap_index+'>'+item.name+'</option>';
    });
    return playerList;
  }
  
  function teeList() {
    var teeList = "";
    if (availableCourseTeesJSON.length == 0) {
      return "";
    }
    if (availableCourseTeesJSON.length == 1) {
      teeList = '<div id="playerTee'+addRowId+'" data-course-tee-slope="'+availableCourseTeesJSON[0].slope+'" data-course-tee-color="'+availableCourseTeesJSON[0].color+'" data-course-tee-id="'+availableCourseTeesJSON[0].id+'" style="background-color:'+availableCourseTeesJSON[0].color+'">'+availableCourseTeesJSON[0].color+'</div>';
    } else {
      teeList = '<div id="playerTee'+addRowId+'" data-course-tee-slope="'+availableCourseTeesJSON[0].slope+'" data-course-tee-color="'+availableCourseTeesJSON[0].color+'" data-course-tee-id="'+availableCourseTeesJSON[0].id+'" class="dropdown">';
      teeList += '  <button id="teeSelectButton'+addRowId+'" class="dropdown-toggle" style="background-color:'+availableCourseTeesJSON[0].color+'" type="button" data-toggle="dropdown" aria-expanded="true"><span class="caret"></span></button>';
      teeList += '  <ul id="courseTees'+addRowId+'" class="dropdown-menu" aria-labelledby="teeSelectButton'+addRowId+'">';
      $.each(availableCourseTeesJSON, function(i, item) {
        teeList += '    <li style="background-color:'+item.color+'"><a href="#" id="courseTeeChangeButton" data-row-id="'+addRowId+'" data-course-tee-slope="'+item.slope+'" data-course-tee-color="'+item.color+'" data-course-tee-id="'+item.id+'">'+item.color+'</a></li>';
      });
      teeList += '  </ul></div>';
    }
    return teeList;
  }

  function addHeaderToScorecard() {
    var headerRow = '<tr>';
    headerRow += '  <th><button id="addRowToScorecard" class="plusMinusButton">+</button></th>';
    headerRow += '  <th>Player</th>';
    headerRow += '  <th>TEE</th>';
    for (var i = 1; i < 10; i++) {
      headerRow += '  <th><input class="scorecardCell" value="0'+i+'" disabled></th>';
    }
    headerRow += '  <th><input class="scorecardCell" value="OUT" disabled></th>';
    for (var i = 10; i < 19; i++) {
      headerRow += '  <th><input class="scorecardCell" value="'+i+'" disabled></th>';
    }
    headerRow += '  <th><input class="scorecardCell" value="IN" disabled></th>';
    headerRow += '  <th><input class="scorecardCell" value="TOT" disabled></th>';
    headerRow += '  <th><input class="scorecardCell" value="HCP" disabled></th>';
    headerRow += '  <th><input class="scorecardCell" value="NET" disabled></th>';
    headerRow += '</tr>';
    $.each(availableCourseTeesJSON, function(i, item) {
      headerRow += '<tr style="background-color:'+item.color+'">';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th>'+item.color+'</th>';
      for (var i = 0; i < 9; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+item.tees[i].yardage+'" disabled></th>';
      }
      headerRow += '  <th><input class="scorecardCell" value="'+item.yardageIn+'" disabled></th>';
      for (var i = 9; i < 18; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+item.tees[i].yardage+'" disabled></th>';
      }
      headerRow += '  <th><input class="scorecardCell" value="'+item.yardageOut+'" disabled></th>';
      headerRow += '  <th><input class="scorecardCell" value="'+item.yardageTotal+'" disabled></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '</tr>';
      headerRow += '<tr style="background-color:'+item.color+'">';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th>Par</th>';
      for (var i = 0; i < 9; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+item.tees[i].par+'" disabled></th>';
      }
      headerRow += '  <th><input class="scorecardCell" value="'+item.parIn+'" disabled></th>';
      for (var i = 9; i < 18; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+item.tees[i].par+'" disabled></th>';
      }
      headerRow += '  <th><input class="scorecardCell" value="'+item.parOut+'" disabled></th>';
      headerRow += '  <th><input class="scorecardCell" value="'+item.parTotal+'" disabled></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '</tr>';
    });
    $("#scorecard thead").append(headerRow);
  }

  function addRowToScorecard() {
    var appendText = '<tr id="scorecardRow'+addRowId+'" data-row-id="'+addRowId+'" data-slope='+availableCourseTeesJSON[0].slope+'>';
    appendText += '<td><button class="plusMinusButton" id="removeRowFromScorecard" data-row-id="'+addRowId+'">-</button></td>';
    appendText += '<td><select id="playerNamesSelect" style="width: 140px" data-row-id="'+addRowId+'"><option>----------------------------</option>'+playerList()+'</select></td><td>'+teeList()+'</td>';
    for (var i = 0; i < 9; i++) {
      appendText += '<td><input class="scorecardCell" id="hole'+i+'" data-hole-number="'+i+'" data-row-id="'+addRowId+'" data-hole-out="'+addRowId+'" type=number min=1 max=99 value='+availableCourseTeesJSON[0].tees[i].par+'></td>';
    }
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalOut'+addRowId+'" value="'+availableCourseTeesJSON[0].parOut+'" disabled></td>';
    for (var i = 9; i < 18; i++) {
      appendText += '<td><input class="scorecardCell" id="hole'+i+'" data-hole-number="'+i+'" data-row-id="'+addRowId+'" data-hole-in="'+addRowId+'" type=number min=1 max=99 value='+availableCourseTeesJSON[0].tees[i].par+'></td>';
    }
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalIn'+addRowId+'" value="'+availableCourseTeesJSON[0].parIn+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="total'+addRowId+'" value="'+availableCourseTeesJSON[0].parTotal+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="hcp'+addRowId+'" value="0" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalNet'+addRowId+'" value="'+availableCourseTeesJSON[0].parTotal+'" disabled></td></tr>';
    $('#scorecard >tbody').append(appendText);
    $('#scorecard #scorecardRow'+addRowId+' #playerNamesSelect').focus();
    addRowId++;
  }
  
  function makeScorecard() {
    $('#scorecard thead').html('');
    addHeaderToScorecard();
    //Load the players for the scorecard scorer, attest
    var nowDate = new Date();
    var nowStr = (nowDate.getMonth()+1<10)?'0':'';
    nowStr += (nowDate.getMonth()+1)+'/';
    nowStr += (nowDate.getDate()<10)?'0':'';
    nowStr += nowDate.getDate()+'/';
    nowStr += nowDate.getFullYear()+' ';
    nowStr += (nowDate.getHours()>12)?(nowDate.getHours()-12):nowDate.getHours()+':';
    nowStr += ((nowDate.getMinutes() < 10)?"0":"")+nowDate.getMinutes()+' ';
    nowStr += ((nowDate.getHours()>12)?'PM':'AM');
    console.log(nowStr);
    console.log(nowDate.getMonth());
    console.log((nowDate.getDate()<10)?'0':''+nowDate.getDate()+'/');
    console.log(nowDate.getFullYear());
    $('#newScorecardFinishTime').val(nowStr);
    $('#newScorecardStartTime').val(nowStr);
    $('#scorecardScorer').empty();
    $('#scorecardAttest').empty();
    $('#newScorecardScorer').val('');
    $('#newScorecardAttest').val('');
    $.each(playersJSON, function(i, item) {
      var option = '<option data-value="'+item.club_member_number+'" value="'+item.name+'"></option>';
      $('#scorecardScorer').append(option);
      $('#scorecardAttest').append(option);
    });
    $('#scorecard tbody').html('');
    addRowToScorecard();
  }

  $(document).ready(function() {

    //TODO: Add the rounds tabs functionality, totals page
    //if (numRounds > 1) {
      var roundTabs = '<ul class="nav nav-tabs">';
      roundTabs += '  <li class="active"><a href="#">Round 1</a></li>';
        for (var i = 2; i <= numRounds; i++) {
        roundTabs += '  <li><a href="#">Round '+i+'</a></li>';
        }
      roundTabs += '  <li><a href="#">Total</a></li>';
      roundTabs += '</ul>';
      $('#roundTabPlaceholder').html(roundTabs);
    //}

    //Load the courses list for select course modal
    $.each(availableCourseTeesJSON, function (i, item) {
      var option = '<option value="'+item.id+'">'+item.name+'</option>';
      $('#enterScorecardCourse').append(option);
    });
    
    //Select course actions
    $('#enterScorecardCourseButton').click(function(event) {
      $('#enterScorecardCourse').modal('hide');
      makeScorecard();
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    //Scorecard actions
    $('#scorecard').on('input', '#scorecardCell', function(event) {
      updateScorecardRound(this);
    });
    $('#scorecard').on('click', '#addRowToScorecard', function(event) {
      addRowToScorecard();
    });
    $('#scorecard').on('click', '#removeRowFromScorecard', function() {
      var rowId = $(this).data('rowId');
      $('#scorecardRow'+rowId).html('');
    });
    $('#scorecard').on('change', '#playerNamesSelect', function(event) {
      var rowId = $(this).data('rowId');
      var hcp = $('option:selected',this).data('handicapIndex');
      if (hcp) {
        $('#hcp'+rowId).val(Math.round(hcp * parseInt($('#scorecardRow'+rowId).data('slope'), 10) / 113));
      } else {
        $('#hcp'+rowId).val(0);
      }
      updateScorecardRound(this);
    });
    $('#scorecard').on('click', '#courseTeeChangeButton', function(event) {
      var rowId = $(this).data('rowId');
      var newSlope = $(this).data('slope');
      var color = $(this).data('color');
      $('#scorecardRow'+rowId).data('slope', newSlope);
      $('#hcp'+rowId).val(Math.round($('#scorecardRow'+rowId+' #playerNamesSelect').data('handicapIndex') * newSlope / 113));
      $('#teeSelectButton'+rowId).css('background-color', color);
      $('#playerTee'+rowId).data('slope', newSlope);
      $('#playerTee'+rowId).data('color', color);
      $('#playerTee'+rowId).data('courseTeeId', $(this).data('courseTeeId'));
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
        var rowId = $(this).data('rowId');
        var clubMemberNumber = $('option:selected',this).val();
        var playerName = $('option:selected',this).text();
        var handicapIndex = $('option:selected',this).data('handicapIndex');
        var courseTeeId = parseInt($('#playerTee'+rowId).data('courseTeeId'), 10);
        var courseHCP = parseInt($('#hcp'+rowId).val(), 10);
        score.clubMemberNumber = clubMemberNumber;
        score.playerName = playerName;
        score.handicapIndex = handicapIndex;
        score.courseTeeId = courseTeeId;
        score.courseHCP = courseHCP;
        
        var holesOut = $('[data-hole-out="'+rowId+'"]');
        var totalOut = 0;
        holesOut.each(function(i, item) {
          var holeNumber = parseInt($(item).data('holeNumber'), 10);
          score['hole'+holeNumber] = parseInt($(item).val(), 10);
          totalOut += parseInt($(item).val(), 10);
        });
        score.totalOut = totalOut;
        var holesIn = $('[data-hole-in="'+rowId+'"]');
        var totalIn = 0;
        holesIn.each(function(i, item) {
          var holeNumber = parseInt($(item).data('holeNumber'), 10);
          score['hole'+holeNumber] = parseInt($(item).val(), 10);
          totalIn += parseInt($(item).val(), 10);
        });
        score.totalIn = totalIn;
        score.total = totalIn+totalOut;
        score.totalNet = totalIn+totalOut-courseHCP;
        scores.push(score);
      });
      var scorer = $('#newScorecardScorer').val();
      var scorerId = $('#scorecardScorer').find('[value="'+scorer+'"]').data('value');
      var attest = $('#newScorecardAttest').val();
      var attestId = $('#scorecardAttest').find('[value="'+attest+'"]').data('value');
      var startTime = $('#newScorecardStartTime').val();
      var finishTime = $('#newScorecardFinishTime').val();
      var context = {
        startTime: moment(startTime).format('YYYY-MM-DD HH:MM'),
        finishTime: moment(finishTime).format('YYYY-MM-DD HH:MM'),
        scorer: scorer,
        scorerId: scorerId,
        attest: attest,
        attestId: attestId,
        tournamentId: tournamentId,
        tournamentName: tournamentName,
        tournamentRoundJSON: JSON.stringify(tournamentRoundsJSON[roundId]),
        scores: JSON.stringify(scores)
      };
      $.post('/golf/calculatescores/', context).done(function(data) {
        $('#loadingDialog').modal('hide');
        $('#enterScorecard').modal('hide');
        console.log(data);
        //TODO: set tables data and styles
      }).fail(function(xhr, textStatus, error) {
        $('#loadingDialog').modal('hide');
        $('#errorDialog').modal({}).show();
        $('#errorHeader').text('failed to store scorecard!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to store scorecard!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });
      $('#loadingDialog').modal('hide');
    });

    //New tournament table
    newTournamentTable = $('#newTournamentTable').DataTable( {
      'dom': 'Bfrtip',
      'buttons': [
        {
          'text': '<u>A</u>dd Scorecard',
          'key': {
            'key': 'a',
            'shiftKey': true
          },
          'action': function ( event, dt, node, config ) {
            event.stopPropagation();
            addRowId = 0;
            if (availableCoursesJSON.length > 1) {
              $('#enterScorecardCourse').modal({backdrop: 'static'}, event.target).show();
            } else {
              makeScorecard();
              $('#enterScorecard').modal({backdrop: 'static'}, event.target).show();
            }
          }
        },
        {
          'text': 'Clear Round Data',
          'action': function ( event, dt, node, config) {
            $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
            var context = {
              tournamentId: tournamentId,
              tournamentName: tournamentName,
              tournamentRoundJSON: tournamentRoundsJSON[roundId],
              roundId: roundId
            };
            $.post('/golf/clearrounddata/', context, function(data) {
              $('#loadingDialog').modal('hide');
              console.log(data);
            }).fail(function(xhr, textStatus, error) {
              $('#loadingDialog').modal('hide');
              $('#errorDialog').modal({}).show();
              $('#errorHeader').text('failed to clear round from scorecard!');
              $('#errorText').text(xhr.responseText);
              console.log('failed to clear round from scorecard!');
              console.log(xhr.responseText);
              console.log(textStatus);
              console.log(error);
            });
          }
        }
      ],
      'scrollY': '65vh',
      'scrollCollapse': false,
      'paging': false,
      'processing': true,
      'language': {
        'processing': '<p class="bg-warning">Processing...</p>',
        "emptyTable": "Add a scorecard!"
      }
    });
    newTournamentTable.buttons().container().append('<b id="tournamentName">Tournament Name: '+tournamentName+'</b>&nbsp;||&nbsp;<b>Date Played: <input type="text" id="roundDate0" value="'+tournamentRoundsJSON[roundId].scheduledDate+'" /></b>');
    $('#newScorecardStartTimePicker').datetimepicker();
    $('#newScorecardFinishTimePicker').datetimepicker();
  });