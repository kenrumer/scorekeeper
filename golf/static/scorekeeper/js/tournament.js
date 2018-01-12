/* global $, tournament, tournamentRounds, players, courses, courseTees, tees, roundId, moment, viewTab, csrf_token */
  var tournamentTable;
  var addRowId = 0;
  var scorecardCourseId = 0;

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
      $('#enterScorecardCourse').modal({backdrop: 'static'}, event.target).show();
    } else {
      $('#scorecard >tbody').html('');
      addRowToScorecard();
      $('#enterScorecard').modal({backdrop: 'static'}, event.target).show();
    }*/
  }

  function editScorecardRow(playerId) {
    /*addRowId = 0;
    if (!courses.length > 1) {
      $('#enterScorecardCourse').modal({backdrop: 'static'}, event.target).show();
    } else {
      $('#scorecard >tbody').html('');
      addRowToScorecard();
      $('#addRowToScorecard').css('display', 'none');
      $('#enterScorecard').modal({backdrop: 'static', keyboard: false}, event.target).show();
    }*/
  }
  
  function playerList() {
    var playerList = "";
    $.each(players, function(i, player) {
      playerList += '<option value='+player.fields.club_member_number+' data-handicap-index='+player.fields.handicap_index+'>'+player.fields.name+'</option>';
    });
    return playerList;
  }
  
  function teeList() {
    var teeList = "";
    if (courseTees.length == 0) {
      return "";
    }
    if (courseTees.length == 1) {
      teeList = '<div id="playerTee'+addRowId+'" data-course-tee-slope="'+courseTees[0].fields.slope+'" data-course-tee-color="'+courseTees[0].fields.color+'" data-course-tee-id="'+courseTees[0].pk+'" style="background-color:'+courseTees[0].fields.color+'">'+courseTees[0].fields.color+'</div>';
    } else {
      teeList = '<div id="playerTee'+addRowId+'" data-course-tee-slope="'+courseTees[0].slope+'" data-course-tee-color="'+courseTees[0].fields.color+'" data-course-tee-id="'+courseTees[0].pk+'" class="dropdown">';
      teeList += '  <button id="teeSelectButton'+addRowId+'" class="dropdown-toggle" style="background-color:'+courseTees[0].fields.color+'" type="button" data-toggle="dropdown" aria-expanded="true"><span class="caret"></span></button>';
      teeList += '  <ul id="courseTees'+addRowId+'" class="dropdown-menu" aria-labelledby="teeSelectButton'+addRowId+'">';
      $.each(courseTees, function(i, courseTee) {
        teeList += '    <li style="background-color:'+courseTee.fields.color+'"><a href="#" id="courseTeeChangeButton" data-row-id="'+addRowId+'" data-course-tee-slope="'+courseTee.fields.slope+'" data-course-tee-color="'+courseTee.fields.color+'" data-course-tee-id="'+courseTee.pk+'">'+courseTee.fields.color+'</a></li>';
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
    $.each(courseTees, function(i, courseTee) {
      var thisTees = tees.filter(function (el) { return el.fields.course_tee == courseTee.pk });
      headerRow += '<tr style="background-color:'+courseTee.fields.color+'">';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th>'+courseTee.fields.color+'</th>';
      var yardageOut = 0;
      for (var i = 0; i < 9; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+thisTees[i].fields.yardage+'" disabled></th>';
        yardageOut += thisTees[i].fields.yardage;
      }
      headerRow += '  <th><input class="scorecardCell" value="'+yardageOut+'" disabled></th>';
      var yardageIn = 0;
      for (var i = 9; i < 18; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+thisTees[i].fields.yardage+'" disabled></th>';
        yardageIn += thisTees[i].fields.yardage;
      }
      headerRow += '  <th><input class="scorecardCell" value="'+yardageIn+'" disabled></th>';
      headerRow += '  <th><input class="scorecardCell" value="'+parseInt(yardageOut+yardageIn, 10)+'" disabled></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '</tr>';
      headerRow += '<tr style="background-color:'+courseTee.fields.color+'">';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th>Par</th>';
      var parOut = 0;
      for (var i = 0; i < 9; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+thisTees[i].fields.par+'" disabled></th>';
        parOut += thisTees[i].fields.par;
      }
      headerRow += '  <th><input class="scorecardCell" value="'+parOut+'" disabled></th>';
      var parIn = 0;
      for (var i = 9; i < 18; i++) {
        headerRow += '  <th><input class="scorecardCell" value="'+thisTees[i].fields.par+'" disabled></th>';
        parIn += thisTees[i].fields.par;
      }
      headerRow += '  <th><input class="scorecardCell" value="'+parIn+'" disabled></th>';
      headerRow += '  <th><input class="scorecardCell" value="'+parseInt(parOut+parIn, 10)+'" disabled></th>';
      headerRow += '  <th></th>';
      headerRow += '  <th></th>';
      headerRow += '</tr>';
    });
    $("#scorecard thead").append(headerRow);
  }

  function addRowToScorecard(courseId) {
    var thisCourseTees = courseTees.filter(function(el) {return el.fields.course = courseId});
    var thisTees = tees.filter(function (el) { return thisCourseTees.indexOf(el.fields.course_tee != -1) });
    var appendText = '<tr id="scorecardRow'+addRowId+'" data-row-id="'+addRowId+'" data-slope='+courseTees[0].fields.slope+'>';
    appendText += '<td><button class="form-control input-sm" id="removeRowFromScorecard" data-row-id="'+addRowId+'">-</button></td>';
    appendText += '<td><select class="form-control input-sm" id="playerNamesSelect" style="width: 140px" data-row-id="'+addRowId+'"><option>----------------------------</option>'+playerList()+'</select></td><td>'+teeList()+'</td>';
    var parOut = 0;
    for (var i = 0; i < 9; i++) {
      appendText += '<td><input class="scorecardCell" id="hole'+i+'" data-hole-number="'+i+'" data-row-id="'+addRowId+'" data-hole-out="'+addRowId+'" type=number min=1 max=99 value='+thisTees[i].par+'></td>';
      parOut += thisTees[i].par;
    }
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalOut'+addRowId+'" value="'+parOut+'" disabled></td>';
    var parIn = 0
    for (var i = 9; i < 18; i++) {
      appendText += '<td><input class="scorecardCell" id="hole'+i+'" data-hole-number="'+i+'" data-row-id="'+addRowId+'" data-hole-in="'+addRowId+'" type=number min=1 max=99 value='+thisTees[i].par+'></td>';
      parIn += thisTees[i].par;
    }
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalIn'+addRowId+'" value="'+parIn+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="total'+addRowId+'" value="'+parIn+parOut+'" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="hcp'+addRowId+'" value="0" disabled></td>';
    appendText += '<td><input class="scorecardCell" data-row-id="'+addRowId+'" id="totalNet'+addRowId+'" value="'+parIn+parOut+'" disabled></td></tr>';
    $('#scorecard >tbody').append(appendText);
    $('#scorecard #scorecardRow'+addRowId+' #playerNamesSelect').focus();
    addRowId++;
  }
  
  function makeScorecard(courseId) {
    $('#scorecard thead').html('');
    addHeaderToScorecard();
    //Load the players for the scorecard scorer, attest
    $('#newScorecardStartTime').val(moment().subtract(3, 'hours').format('MM/DD/YYYY hh:ss A'));
    $('#newScorecardFinishTime').val(moment().format('MM/DD/YYYY hh:ss A'));
    $('#scorecardScorer').empty();
    $('#scorecardAttest').empty();
    $('#newScorecardScorer').val('');
    $('#newScorecardAttest').val('');
    $.each(players, function(i, player) {
      var option = '<option data-value="'+player.fields.club_member_number+'" value="'+player.fields.name+'"></option>';
      $('#scorecardScorer').append(option);
      $('#scorecardAttest').append(option);
    });
    $('#scorecard tbody').html('');
    addRowToScorecard(courseId);
  }

  function showNetTab() {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    var context = {
      tournament: JSON.stringify(tournament),
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
      $('#errorText').text(xhr.status + ' ' + error);
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
      tournament: JSON.stringify(tournament),
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
      $('#errorText').text(xhr.status + ' ' + error);
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
      tournament: JSON.stringify(tournament),
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
      $('#errorText').text(xhr.status + ' ' + error);
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
    $('#roundName').text(tournament.fields.name);
    $('#roundDate').val(month+'/'+day+'/'+d.getFullYear());
    var roundTabs = '<ul class="nav nav-tabs navbar-right">';
    for (var i = 0; i < tournamentRounds.length; i++) {
      if (roundId == i) {
        roundTabs += '  <li class="active" data-toggle="tab"><a href="#">'+tournamentRounds[i].fields.name+'</a></li>';
      } else {
        roundTabs += '  <li data-toggle="tab"><a href="#">'+tournamentRounds[i].fields.name+'</a></li>';
      }
    }
    if (tournamentRounds.length > 1) {
      roundTabs += '  <li data-toggle="tab"><a href="#">Total</a></li>';
    }
    roundTabs += '</ul>';
    $('#roundTabPlaceholder').html(roundTabs);

    $('#netScoresTab a').click(function(event) {
      showNetTab();
    });

    $('#grossScoresTab a').click(function(event) {
      showGrossTab();
    });

    $('#payoutTab a').click(function(event) {
      showPayoutTab();
    });
    
    //Load the courses list for select course modal
    $.each(courses, function(i, course) {
      var option = '<option value="'+course.pk+'">'+course.fields.name+'</option>';
      $('#enterScorecardCourses').append(option);
    });
    
    //Select course actions
    $('#enterScorecardCourseButton').click(function(event) {
      $('#enterScorecardCourse').modal('hide');
      //Get the selected course and build the scorecard, I think pass the pk to makescorecard...
      scorecardCourseId = $('#enterScorecardCourses').val();
      makeScorecard(scorecardCourseId);
      $('#enterScorecard').modal({backdrop: 'static'}, event.target).show();
    });

    //Scorecard actions
    $('#scorecard').on('input', '#scorecardCell', function(event) {
      updateScorecardRound(this);
    });
    $('#scorecard').on('click', '#addRowToScorecard', function(event) {
      addRowToScorecard(scorecardCourseId);
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
      var scplayers = [];
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
        scplayers.push(player);
      });
      var scorecard = {};
      scorecard.scorer = $('#newScorecardScorer').val();
      scorecard.scorerId = $('#scorecardScorer').find('[value="'+scorecard.scorer+'"]').data('value');
      scorecard.attest = $('#newScorecardAttest').val();
      scorecard.attestId = $('#scorecardAttest').find('[value="'+scorecard.attest+'"]').data('value');
      scorecard.startTime = moment($('#newScorecardStartTime').val()).format('YYYY-MM-DD HH:MM');
      scorecard.finishTime = moment($('#newScorecardFinishTime').val()).format('YYYY-MM-DD HH:MM');
      var context = {
        tournamentId: tournament.pk,
        tournamentName: tournament.fields.name,
        tournamentRound: JSON.stringify(tournamentRounds[roundId]),
        scorecard: JSON.stringify(scorecard),
        players: JSON.stringify(scplayers),
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
        $('#errorText').text(xhr.status + ' ' + error);
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
            if (courses.length > 1) {
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
              $('#errorText').text(xhr.status + ' ' + error);
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
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
      }
    });
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