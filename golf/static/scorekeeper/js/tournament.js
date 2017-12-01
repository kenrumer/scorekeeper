/* global $, tournamentId, tournamentName, roundCount, tournamentRounds, players, availableCourses, availableCourseTees, roundId, moment, viewTab */
  var tournamentTable;
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
    $.each(players, function(i, item) {
      playerList += '<option value='+item.club_member_number+' data-handicap-index='+item.handicap_index+'>'+item.name+'</option>';
    });
    return playerList;
  }
  
  function teeList() {
    var teeList = "";
    if (availableCourseTees.length == 0) {
      return "";
    }
    if (availableCourseTees.length == 1) {
      teeList = '<div id="playerTee'+addRowId+'" data-course-tee-slope="'+availableCourseTees[0].slope+'" data-course-tee-color="'+availableCourseTees[0].color+'" data-course-tee-id="'+availableCourseTees[0].id+'" style="background-color:'+availableCourseTees[0].color+'">'+availableCourseTees[0].color+'</div>';
    } else {
      teeList = '<div id="playerTee'+addRowId+'" data-course-tee-slope="'+availableCourseTees[0].slope+'" data-course-tee-color="'+availableCourseTees[0].color+'" data-course-tee-id="'+availableCourseTees[0].id+'" class="dropdown">';
      teeList += '  <button id="teeSelectButton'+addRowId+'" class="dropdown-toggle" style="background-color:'+availableCourseTees[0].color+'" type="button" data-toggle="dropdown" aria-expanded="true"><span class="caret"></span></button>';
      teeList += '  <ul id="courseTees'+addRowId+'" class="dropdown-menu" aria-labelledby="teeSelectButton'+addRowId+'">';
      $.each(availableCourseTees, function(i, item) {
        teeList += '    <li style="background-color:'+item.color+'"><a href="#" id="courseTeeChangeButton" data-row-id="'+addRowId+'" data-course-tee-slope="'+item.slope+'" data-course-tee-color="'+item.color+'" data-course-tee-id="'+item.id+'">'+item.color+'</a></li>';
      });
      teeList += '  </ul></div>';
    }
    return teeList;
  }

  function addHeaderToScorecard() {
    var headerRow = '<tr>';
    headerRow += '  <th><button id="addRowToScorecard" class="form-control input-sm">+</button></th>';
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
    $.each(availableCourseTees, function(i, item) {
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
    var appendText = '<tr id="scorecardRow'+addRowId+'" data-row-id="'+addRowId+'" data-slope='+availableCourseTees[0].slope+'>';
    appendText += '<td><button class="form-control input-sm" id="removeRowFromScorecard" data-row-id="'+addRowId+'">-</button></td>';
    appendText += '<td><select class="form-control input-sm" id="playerNamesSelect" style="width: 140px" data-row-id="'+addRowId+'"><option>----------------------------</option>'+playerList()+'</select></td><td>'+teeList()+'</td>';
    for (var i = 0; i < 9; i++) {
      appendText += '<td><input class="scorecardCell" id="hole'+i+'" data-hole-number="'+i+'" data-row-id="'+addRowId+'" data-hole-out="'+addRowId+'" type=number min=1 max=99 value='+availableCourseTees[0].tees[i].par+'></td>';
    }
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalOut'+addRowId+'" value="'+availableCourseTees[0].parOut+'" disabled></td>';
    for (var i = 9; i < 18; i++) {
      appendText += '<td><input class="scorecardCell" id="hole'+i+'" data-hole-number="'+i+'" data-row-id="'+addRowId+'" data-hole-in="'+addRowId+'" type=number min=1 max=99 value='+availableCourseTees[0].tees[i].par+'></td>';
    }
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalIn'+addRowId+'" value="'+availableCourseTees[0].parIn+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="total'+addRowId+'" value="'+availableCourseTees[0].parTotal+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="hcp'+addRowId+'" value="0" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalNet'+addRowId+'" value="'+availableCourseTees[0].parTotal+'" disabled></td></tr>';
    $('#scorecard >tbody').append(appendText);
    $('#scorecard #scorecardRow'+addRowId+' #playerNamesSelect').focus();
    addRowId++;
  }
  
  function makeScorecard() {
    $('#scorecard thead').html('');
    addHeaderToScorecard();
    //Load the players for the scorecard scorer, attest
    $('#newScorecardStartTime').val(moment().subtract(3, 'hours').format('MM/DD/YYYY hh:ss A'));
    $('#newScorecardFinishTime').val(moment().format('MM/DD/YYYY hh:ss A'));
    $('#scorecardScorer').empty();
    $('#scorecardAttest').empty();
    $('#newScorecardScorer').val('');
    $('#newScorecardAttest').val('');
    $.each(players, function(i, item) {
      var option = '<option data-value="'+item.club_member_number+'" value="'+item.name+'"></option>';
      $('#scorecardScorer').append(option);
      $('#scorecardAttest').append(option);
    });
    $('#scorecard tbody').html('');
    addRowToScorecard();
  }
  function showNetTab() {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    var context = {
      tournamentId: tournamentId,
      tournamentName: tournamentName,
      tournamentRound: JSON.stringify(tournamentRounds[roundId]),
      viewTab: 'net'
    };
    $.post('/golf/getscores/', context).done(function(data) {
      console.log(data);
      $('#payoutForm').hide();
      $('#tournamentTableWrapper').show();
      tournamentTable.clear();
      $.each(data.rows, function(i, item) {
        var row = tournamentTable.row.add(item);
        var rowNode = row.node();
        $.each(data.styles[i], function(j, item1) {
          if (j < 9) {
            var thisTD = $(rowNode).find('td').eq(4+j);
            thisTD.css(item1.split(':')[0], item1.split(':')[1]);
          } else {
            var thisTD = $(rowNode).find('td').eq(5+j);
            thisTD.css(item1.split(':')[0], item1.split(':')[1]);
          }
        });
      });
      tournamentTable.draw();
      viewTab = 'net';
    }).fail(function(xhr, textStatus, error) {
      $('#errorDialog').modal({}).show();
      $('#errorHeader').text('failed to load net scores!');
      $('#errorText').text(xhr.responseText);
      console.log('failed to load net scores!');
      console.log(xhr.responseText);
      console.log(textStatus);
      console.log(error);
    }).always(function(a, textStatus, b) {
      $('#loadingDialog').modal('hide');
    });
  }

  function showGrossTab() {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    var context = {
      tournamentId: tournamentId,
      tournamentName: tournamentName,
      tournamentRound: JSON.stringify(tournamentRounds[roundId]),
      viewTab: 'gross'
    };
    $.post('/golf/getscores/', context).done(function(data) {
      console.log(data);
      $('#payoutForm').hide();
      $('#tournamentTableWrapper').show();
      tournamentTable.clear();
      $.each(data.rows, function(i, item) {
        var row = tournamentTable.row.add(item);
        var rowNode = row.node();
        $.each(data.styles[i], function(j, item1) {
          if (j < 9) {
            var thisTD = $(rowNode).find('td').eq(4+j);
            thisTD.css(item1.split(':')[0], item1.split(':')[1]);
          } else {
            var thisTD = $(rowNode).find('td').eq(5+j);
            thisTD.css(item1.split(':')[0], item1.split(':')[1]);
          }
        });
      });
      tournamentTable.draw();
      viewTab = 'gross';
    }).fail(function(xhr, textStatus, error) {
      $('#errorDialog').modal({}).show();
      $('#errorHeader').text('failed to load gross scores!');
      $('#errorText').text(xhr.responseText);
      console.log('failed to load gross scores!');
      console.log(xhr.responseText);
      console.log(textStatus);
      console.log(error);
    }).always(function(a, textStatus, b) {
      $('#loadingDialog').modal('hide');
    });
  }

  function showPayoutTab() {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    var context = {
      tournamentId: tournamentId,
      tournamentName: tournamentName,
      roundId: roundId,
      tournamentRound: JSON.stringify(tournamentRounds[roundId])
    };
    $.post('/golf/getpayout/', context).done(function(data) {
      viewTab = 'payout';
      $('#tournamentTableWrapper').hide();
      $('#tournamentPayoutWrapper').html(data);
      $('#tournamentPayoutWrapper').show();
    }).fail(function(xhr, textStatus, error) {
      $('#errorDialog').modal({}).show();
      $('#errorHeader').text('failed to load payout!');
      $('#errorText').text(xhr.responseText);
      console.log('failed to load payout!');
      console.log(xhr.responseText);
      console.log(textStatus);
      console.log(error);
    }).always(function(a, textStatus, b) {
      $('#loadingDialog').modal('hide');
    });
  }

  /* Will put this back in after testing
  $(window).on('beforeunload', function(event) {
    return 'are you sure you want to leave?';
  });*/

  $(document).ready(function() {

    var d = new Date();
    var month = (d.getMonth()<9)?'0'+d.getMonth()+1:d.getMonth()+1;
    var day = (d.getDate()<10)?'0'+d.getDate():d.getDate();
    $('#roundDate').val(month+'/'+day+'/'+d.getFullYear());
    //TODO: Add the rounds tabs functionality, totals page
    var roundTabs = '<ul class="nav nav-tabs navbar-right">';
    for (var i = 0; i < roundCount; i++) {
      if (roundId == i) {
        roundTabs += '  <li class="active" data-toggle="tab"><a href="#">'+tournamentRounds[i].name+'</a></li>';
      } else {
        roundTabs += '  <li data-toggle="tab"><a href="#">'+tournamentRounds[i].name+'</a></li>';
      }
    }
    if (roundCount > 1) {
      roundTabs += '  <li data-toggle="tab"><a href="#">Total</a></li>';
    }
    roundTabs += '</ul>';
    $('#roundTabPlaceholder').html(roundTabs);

    $('#netScoresTab a').click(function(event) {
      showNetTab();
    });

    $('#grossScoresTab').click(function(event) {
      showGrossTab();
    });

    $('#payoutTab a').click(function(event) {
      showPayoutTab();
    });
    
    //Load the courses list for select course modal
    $.each(availableCourseTees, function (i, item) {
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
      var players = [];
      $('#scorecard #playerNamesSelect').each(function() {
        var player = {};
        var rowId = $(this).data('rowId');
        var courseHCP = parseInt($('#hcp'+rowId).val(), 10);
        player.clubMemberNumber = $('option:selected',this).val();
        player.playerName = $('option:selected',this).text();
        player.handicapIndex = $('option:selected',this).data('handicapIndex');
        player.round = {};
        player.round.courseTeeId = parseInt($('#playerTee'+rowId).data('courseTeeId'), 10);
        player.round.courseHCP = courseHCP;
        
        var totalOut = 0;
        player.round.score = {};
        var holesOut = $('[data-hole-out="'+rowId+'"]');
        holesOut.each(function(i, item) {
          player.round.score['hole'+parseInt($(item).data('holeNumber'), 10)] = parseInt($(item).val(), 10);
          totalOut += parseInt($(item).val(), 10);
        });
        player.round.totalOut = totalOut;
        var totalIn = 0;
        var holesIn = $('[data-hole-in="'+rowId+'"]');
        holesIn.each(function(i, item) {
          player.round.score['hole'+parseInt($(item).data('holeNumber'), 10)] = parseInt($(item).val(), 10);
          totalIn += parseInt($(item).val(), 10);
        });
        player.round.totalIn = totalIn;
        player.round.total = totalIn+totalOut;
        player.round.totalNet = totalIn+totalOut-courseHCP;
        players.push(player);
      });
      var scorecard = {};
      scorecard.scorer = $('#newScorecardScorer').val();
      scorecard.scorerId = $('#scorecardScorer').find('[value="'+scorecard.scorer+'"]').data('value');
      scorecard.attest = $('#newScorecardAttest').val();
      scorecard.attestId = $('#scorecardAttest').find('[value="'+scorecard.attest+'"]').data('value');
      scorecard.startTime = moment($('#newScorecardStartTime').val()).format('YYYY-MM-DD HH:MM');
      scorecard.finishTime = moment($('#newScorecardFinishTime').val()).format('YYYY-MM-DD HH:MM');
      var context = {
        tournamentId: tournamentId,
        tournamentName: tournamentName,
        tournamentRound: JSON.stringify(tournamentRounds[roundId]),
        scorecard: JSON.stringify(scorecard),
        players: JSON.stringify(players),
        viewTab: viewTab
      };
      $.post('/golf/updatescores/', context).done(function(data) {
        tournamentTable.clear();
        $.each(data.rows, function(i, item) {
          var rowNode = tournamentTable.row.add(item).node();
          $.each(data.styles[i], function(j, item1) {
            if (j < 9) {
              var thisTD = $(rowNode).find('td').eq(4+j);
              var styles = item1.split(' ');
              for (var k = 0; k < styles.length; k++) {
                thisTD.css(item1[k].split(':')[0], item1[k].split(':')[1]);
              }
            } else {
              var thisTD = $(rowNode).find('td').eq(5+j);
              var styles = item1.split(' ');
              console.log(styles)
              for (var k = 0; k < styles.length; k++) {
                thisTD.css(item1[k].split(':')[0], item1[k].split(':')[1]);
              }
            }
          });
        });
        tournamentTable.draw();
        $('#enterScorecard').modal('hide');
      }).fail(function(xhr, textStatus, error) {
        $('#errorDialog').modal({}).show();
        $('#errorHeader').text('failed to store scorecard!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to store scorecard!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      }).always(function() {
        $('#loadingDialog').modal('hide');
      });
    });

    //tournament table
    tournamentTable = $('#tournamentTable').DataTable( {
      'dom': 'Bf<"customTitle">rtip',
      'buttons': [
        {
          'text': '<u>A</u>dd Scorecard',
          'key': {
            'key': 'a',
            'shiftKey': true
          },
          'action': function ( event, dt, node, config ) {
            event.stopPropagation();
            if (availableCourses.length > 1) {
              $('#enterScorecardCourse').modal({backdrop: 'static'}, event.target).show();
            } else {
              addRowId = 0;
              makeScorecard();
              $('#enterScorecard').modal({backdrop: 'static'}, event.target).show();
            }
          }
        },
        {
          'text': '<u>P</u>rint',
          'key': {
            'key': 'r',
            'shiftKey': true
          },
          'action': function ( event, dt, node, config) {
            event.stopPropagation();
            $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
            //var context = {
            //  tournamentId: tournamentId
            //};
            window.open('/golf/printtournament/');
          }
        },
        {
          'text': '<u>C</u>lear Round Data',
          'key': {
            'key': 'c',
            'shiftKey': true
          },
          'action': function ( event, dt, node, config) {
            event.stopPropagation();
            $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
            var context = {
              tournamentRound: JSON.stringify(tournamentRounds[roundId]),
            };
            $.post('/golf/clearrounddata/', context).done(function(data) {
              tournamentTable.clear();
              console.log(data);
            }).fail(function(xhr, textStatus, error) {
              $('#errorDialog').modal({}).show();
              $('#errorHeader').text('failed to clear round from scorecard!');
              $('#errorText').text(xhr.responseText);
              console.log('failed to clear round from scorecard!');
              console.log(xhr.responseText);
              console.log(textStatus);
              console.log(error);
            }).always(function(a, textStatus, b) {
              $('#loadingDialog').modal('hide');
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

    if (viewTab == 'net') {
      $('#netScoresTab').trigger('click');
      $('#tournamentTableWrapper').show();
      $('#payoutForm').hide();
    }
    showNetTab();
    if (viewTab == 'gross') {
      $('#grossScoresTab').trigger('click');
      $('#tournamentTableWrapper').show();
      $('#payoutForm').hide();
    }
    if (viewTab == 'payout') {
      $('#payoutTab').trigger('click');
      $('#tournamentTableWrapper').hide();
      $('#payoutForm').show();
    }
    $('#newScorecardStartTimePicker').datetimepicker();
    $('#newScorecardFinishTimePicker').datetimepicker();
  });