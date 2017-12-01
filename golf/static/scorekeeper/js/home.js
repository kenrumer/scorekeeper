/* global $, club, courses, courseTees, tournaments, tournamentRounds, formatPlugins, players, playerPlugins, activities, moment */
  var newTournamentCoursesAvailableCourseList = [];
  var newTournamentCoursesSelectedCourseList = [];
  var newTournamentCourseTeesAvailableCourseTeeList = [];
  var newTournamentCourseTeesSelectedCourseTeeList = [];

  $(document).ready(function() {
  
    $('#titleClubName').html(club.name);
    $('#playerLoadDate').html(moment(club.players_last_updated).format('MM/DD/YYYY hh:mm A'));
    //Menu buttons
    //New Tournament Wizard
    $('#newTournamentButton').click(function(event) {
      $('#newTournamentName').val(club.default_tournament_name+' - '+moment().format('MM/DD/YYYY'));
      $('#newTournamentRoundCount').val(1);
      $('#newTournament').modal({backdrop: 'static'}, event.target).show();
    });
  
    $('#newTournamentNextButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {
        tournamentName: $('#newTournamentName').val()
      };
      $.post('/golf/checkfortournamentduplicate/', context).done(function(data) {
        var duplicate = data.duplicate;
        if (duplicate == true) {
          $('#newTournamentDuplicate').modal({backdrop: 'static', keyboard: false}, event.target).show();
        } else {
          context = {};
          $.post('/golf/getallformatplugins/', context).done(function(data) {
            var formatPlugins = data.formatPlugins;
            $('#newTournament').modal('hide');
            var roundCount = parseInt($('#newTournamentRoundCount').val(), 10);
            $('#newTournamentRoundsPlaceholder').html('');
            var roundsInput = '<div class="list-group newTournamentRoundsList">';
            for (var i = 1; i <= roundCount; i++) {
              roundsInput += '  <div class="row" id="newTournamentRoundsListItem'+i+'">';
             	roundsInput += '    <div class="col-sm-1"></div>';
             	roundsInput += '    <div class="col-sm-3">';
             	roundsInput += '      <input type="text" class="form-control" id="newTournamentRoundsName'+i+'" value="Round '+i+'" />';
              roundsInput += '    </div>';
             	roundsInput += '    <div class="col-sm-3">';
             	roundsInput += '       <select class="form-control" id="newTournamentRoundsFormatPlugin'+i+'">';
              $.each(formatPlugins, function (i, item) {
             	  roundsInput += '          <option value="'+item.id+'">'+item.name+'</option>';
              });
             	roundsInput += '       </select>';
             	roundsInput += '    </div>';
              roundsInput += '    <div class="col-sm-3 input-group date" style="z-index: 999;" id="newTournamentRoundsScheduledDatePicker'+i+'">';
              roundsInput += '      <input type="text" class="form-control" id="newTournamentRoundsScheduledDate'+i+'" value="'+moment().format('MM/DD/YYYY')+'" />';
              roundsInput += '      <span class="input-group-addon">';
              roundsInput += '        <span class="glyphicon glyphicon-calendar"></span>';
              roundsInput += '      </span>';
              roundsInput += '    </div>';
             	roundsInput += '    <div class="col-sm-1"></div>';
              roundsInput += '  </div>';
            }
            roundsInput += '</div>';
            $('#newTournamentRoundsPlaceholder').append(roundsInput);
            for (var i = 1; i <= roundCount; i++) {
              $('#newTournamentRoundsPlaceholder').find('#newTournamentRoundsScheduledDatePicker'+i).datetimepicker({format: 'MM/DD/YYYY'});
            }
            $('#newTournamentRounds').modal({backdrop: 'static'}, event.target).show();
          }).fail(function(xhr, textStatus, error) {
            $('#newTournament').modal('hide');
            $('#errorHeader').text('failed to load format plugins!');
            $('#errorText').text(xhr.responseText);
            console.log('failed to load format plugins!');
            console.log(xhr.responseText);
            console.log(textStatus);
            console.log(error);
            $('#errorDialog').modal({}).show();
          }).always(function(a, textStatus, b) {
            $('#newTournament').modal('hide');
            $('#loadingDialog').modal('hide');
          });
        }
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to determine if this is a duplicate tournament!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to determine if this is a duplicate tournament!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#newTournament').modal('hide');
        $('#loadingDialog').modal('hide');
      });
    });
  
    $('#newTournamentDuplicateCancelTournament').click(function(event) {
      $('#newTournamentDuplicate').modal('hide');
      $('#newTournament').modal('hide');
    });
    $('#newTournamentDuplicateCreateNewTournament').click(function(event) {
      $('#newTournamentDuplicate').modal('hide');
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/getallformatplugins/', context).done(function(data) {
        var formatPlugins = data.formatPlugins;
        var roundCount = parseInt($('#newTournamentRoundCount').val(), 10);
        //Show choose dates
        $('#newTournamentRoundsPlaceholder').html('');
        var roundsInput = '<div class="list-group newTournamentRoundsList">';
        for (var i = 1; i <= roundCount; i++) {
          roundsInput += '  <div class="row" id="newTournamentRoundsListItem'+i+'">';
         	roundsInput += '    <div class="col-sm-1"></div>';
         	roundsInput += '    <div class="col-sm-3">';
         	roundsInput += '      <input type="text" class="form-control" id="newTournamentRoundsName'+i+'" value="Round '+i+'" />';
          roundsInput += '    </div>';
         	roundsInput += '    <div class="col-sm-3">';
         	roundsInput += '       <select class="form-control" id="newTournamentRoundsFormatPlugin'+i+'">';
          $.each(formatPlugins, function (i, item) {
         	  roundsInput += '          <option value="'+item.id+'">'+item.name+'</option>';
          });
         	roundsInput += '       </select>';
         	roundsInput += '    </div>';
          roundsInput += '    <div class="col-sm-3 input-group date" style="z-index: 999;" id="newTournamentRoundsScheduledDatePicker'+i+'">';
          roundsInput += '      <input type="text" class="form-control" id="newTournamentRoundsScheduledDate'+i+'" value="'+moment().format('MM/DD/YYYY')+'" />';
          roundsInput += '      <span class="input-group-addon">';
          roundsInput += '        <span class="glyphicon glyphicon-calendar"></span>';
          roundsInput += '      </span>';
          roundsInput += '    </div>';
         	roundsInput += '    <div class="col-sm-1"></div>';
          roundsInput += '  </div>';
        }
        roundsInput += '</div>';
        $('#newTournamentRoundsPlaceholder').append(roundsInput);
        for (var i = 1; i <= roundCount; i++) {
          $('#newTournamentRoundsPlaceholder').find('#newTournamentRoundsScheduledDatePicker'+i).datetimepicker({format: 'MM/DD/YYYY'});
        }
        $('#newTournamentRounds').modal({backdrop: 'static'}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to load format plugins!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to load format plugins!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#newTournament').modal('hide');
        $('#loadingDialog').modal('hide');
      });
      $('#newTournamentRounds').modal({backdrop: 'static'}, event.target).show();
    });
  
    $('#newTournamentRoundsBackButton').click(function(event) {
      $('#newTournamentRounds').modal('hide');
      $('#newTournament').modal({backdrop: 'static'}, event.target).show();
    });
    $('#newTournamentRoundsNextButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/getallcourses/', context).done(function(data) {
        var courses = data.courses;
        $('#newTournamentCoursesMS').multiSelect('refresh');
        newTournamentCoursesSelectedCourseList = [];
        newTournamentCoursesAvailableCourseList = courses;
        $.each(courses, function (i, item) {
          if (item.default) {
            $('#newTournamentCoursesMS').multiSelect('addOption', { value: item.id, text: item.name });
            $('#newTournamentCoursesMS').multiSelect('select', item.id.toString());
          } else {
            $('#newTournamentCoursesMS').multiSelect('addOption', { value: item.id, text: item.name });
          }
        });
        $('#newTournamentCourses').modal({backdrop: 'static'}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to load courses!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to load courses!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#newTournamentRounds').modal('hide');
        $('#loadingDialog').modal('hide');
      });
    });
  
    $('#newTournamentCoursesBackButton').click(function(event) {
      $('#newTournamentCourses').modal('hide');
      $('#newTournamentRounds').modal({backdrop: 'static'}, event.target).show();
    });
    $('#newTournamentCoursesNextButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {
        courses: JSON.stringify(newTournamentCoursesSelectedCourseList)
      };
      $.post('/golf/getcoursetees/', context).done(function(data) {
        var courseTees = data.courseTees;
        newTournamentCourseTeesSelectedCourseTeeList = [];
        newTournamentCourseTeesAvailableCourseTeeList = courseTees;
        $('#newTournamentCourseTeesMS').multiSelect('refresh');
        $.each(courseTees, function (i, item) {
          if (item.default) {
            $('#newTournamentCourseTeesMS').multiSelect('addOption', { value: item.id, text: item.course__name+' - '+item.name });
            $('#newTournamentCourseTeesMS').multiSelect('select', item.id.toString());
          } else {
            $('#newTournamentCourseTeesMS').multiSelect('addOption', { value: item.id, text: item.course__name+' - '+item.name });
          }
        });
        $('#newTournamentCourseTees').modal({backdrop: 'static'}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#newTournament').modal('hide');
        $('#errorHeader').text('failed to load course tees!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to load course tees!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#newTournamentCourses').modal('hide');
        $('#loadingDialog').modal('hide');
      });
    });
  
    $('#newTournamentCourseTeesBackButton').click(function(event) {
      $('#newTournamentCourseTees').modal('hide');
      $('#newTournamentCourses').modal({backdrop: 'static'}, event.target).show();
    });
    $('#newTournamentCourseTeesNextButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var roundCount = parseInt($('#newTournamentRoundCount').val(), 10);
      var tournamentRounds = [];
      for (var i = 1; i <= roundCount; i++) {
        var tournamentRound = {
          formatId: $('#newTournamentRoundsFormatPlugin'+i).val(),
          scheduledDate: $('#newTournamentRoundsScheduledDate'+i).val(),
          name: $('#newTournamentRoundsName'+i).val()
        };
        tournamentRounds.push(tournamentRound);
      }
      var context = {
        tournamentName: $('#newTournamentName').val(),
        tournamentRounds: JSON.stringify(tournamentRounds),
        roundCount: roundCount,
        availableCourses: JSON.stringify(newTournamentCoursesSelectedCourseList),
        availableCourseTees: JSON.stringify(newTournamentCourseTeesSelectedCourseTeeList)
      };
      $.post('/golf/newtournament/', context).done(function(data) {
        $.redirect('/golf/tournament/', data, 'POST', '', true);
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to create a tournament!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to create a tournament!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#newTournamentCourseTees').modal('hide');
        $('#loadingDialog').modal('hide');
      });
    });
  
    //Edit Tournament
    $('#editTournamentButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/getalltournaments/', context).done(function(data) {
        var tournaments = data.tournaments;
        var tournamentRows = '';
        $.each(tournaments, function(i, item) {
          var tournamentRow = '<div class="list-group-item editTournamentListItem" style="padding:0px 0px 0px 0px;" id="editTournamentListItem" tournament-name="'+item.name+'" data-tournament-id="'+item.id+'">';
          tournamentRow += '  <div class="row">';
          tournamentRow += '    <div class="col-sm-1"></div>';
          tournamentRow += '    <div class="col-sm-10">';
          tournamentRow += '      <div class="input-group">';
          tournamentRow += '        <div class="input-group-btn">';
          tournamentRow += '          <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Action <span class="caret"></span></button>';
          tournamentRow += '          <ul class="dropdown-menu">';
          tournamentRow += '            <li><a href="#">Edit</a></li>';
          tournamentRow += '            <li><a href="#">Export</a></li>';
          tournamentRow += '            <li><a href="#">Print</a></li>';
          tournamentRow += '            <li role="separator" class="divider"></li>';
          tournamentRow += '            <li><a href="#">Delete</a></li>';
          tournamentRow += '          </ul>';
          tournamentRow += '        </div>';
          tournamentRow += '   	    <input id="editTournamentId" type="number" class="form-control input-group-addon editTournamentId" style="text-align:right;background-color:#fff;" value="'+item.id+'" data-original-value="'+item.id+'" readOnly disabled />';
          tournamentRow += '   	    <span class="input-group-btn" style="width:0px;"></span>';
          tournamentRow += '   	    <input id="editTournamentName" type="text" class="form-control input-group-addon editTournamentName" style="text-align:left;background-color:#fff;" value="'+item.name+'" data-original-value="'+item.name+'" />';
          tournamentRow += '   	    <span class="input-group-btn" style="width:0px;"></span>';
          tournamentRow += '   	    <input id="editTournamentStartDate" type="text" class="form-control input-group-addon editTournamentStartDate" style="text-align:left;background-color:#fff;" value="'+moment(item.start_time).format('MM/DD/YYYY')+'" data-original-value="'+moment(item.start_time).format('MM/DD/YYYY')+'" />';
          tournamentRow += '   	    <span class="input-group-btn" style="width:0px;"></span>';
          tournamentRow += '   	    <input id="editTournamentFinishDate" type="text" class="form-control input-group-addon editTournamentFinishDate" style="text-align:left;background-color:#fff;" value="'+moment(item.finish_time).format('MM/DD/YYYY')+'" data-original-value="'+moment(item.finish_time).format('MM/DD/YYYY')+'" />';
          tournamentRow += '   	  </div>';
          tournamentRow += '    </div>';
          tournamentRow += '    <div class="col-sm-1"></div>';
          tournamentRow += '  </div>';
          tournamentRow += '</div>';
          tournamentRows += tournamentRow;
        });
        $('#editTournamentList').html(tournamentRows);
        $('#editTournament').modal({backdrop: 'static'}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to get all tournaments!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to get all tournaments!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#loadingDialog').modal('hide');
      });
    });
  	function updateEditTournamentList() {
  		$('.editTournamentListItem').show();
    	var currentQuery = $('#editTournamentSearchInput').val().toUpperCase();
    	if (currentQuery !== '') {
      	$('.editTournamentListItem').each(function(index) {
      	  var currentKeyword = $(this).find('.editTournamentName').val().toUpperCase();
      	  var currentKeywordOriginal = $(this).find('.editTournamentName').data('originalValue').toUpperCase();
        	if (currentKeyword.indexOf(currentQuery) === -1) {
        		$(this).hide();
        	} else {
          	if (currentKeywordOriginal.indexOf(currentQuery) === -1) {
          		$(this).hide();
          	}
        	}
      	});
    	}
  	  var currentStartQuery;
  	  if ($('#editTournamentSearchStartDate').val() !== '') {
  	    currentStartQuery = moment($('#editTournamentSearchStartDate').val());
  	  } else {
  	    currentStartQuery = moment(0);
  	  }
  	  var currentFinishQuery;
  	  if ($('#editTournamentSearchFinishDate').val() !== '') {
  	    currentFinishQuery = moment($('#editTournamentSearchFinishDate').val());
  	  } else {
  	    currentFinishQuery = moment(new Date()).add(10, 'year');
  	  }
  	  $('.editTournamentListItem').each(function(event) {
  	    if ($(this).is(':visible')) {
    	    if ((currentStartQuery.isAfter($(this).find('.editTournamentStartDate').val())) || (currentFinishQuery.isBefore($(this).find('.editTournamentFinishDate').val()))) {
    	      $(this).hide();
    	    }
  	    }
	    });
  	}
    $('#editTournamentSearchInput').keyup(function(event){
  	  updateEditTournamentList();
  	});
  	$('#editTournamentSearchStartDateDateTimePicker').on("dp.change", function(event) {
  	  updateEditTournamentList();
  	});
  	$('#editTournamentSearchFinishDateDateTimePicker').on("dp.change", function(event) {
  	  updateEditTournamentList();
  	});
    $('#saveTournamentsButton').click(function(event){
      window.location.href = '/golf/edittournament/0';
    });
  
    //Load Players
    $('#loadPlayersButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/loadplayers/', context).done(function(data) {
        $('#loadingDialog').modal('hide');
        var d = new Date();
        var day = (d.getDate()<10)?'0'+d.getDate():d.getDate();
        var month = (d.getMonth()<10)?'0'+d.getMonth()+1:d.getMonth()+1;
        var year = d.getFullYear();
        var tmpHour = (d.getHours()>12)?d.getHours()-12:d.getHours();
        var hour = (tmpHour<10)?'0'+tmpHour:tmpHour;
        var minutes = d.getMinutes();
        var ampm = (d.getHours()>12)?'PM':'AM';
        $('#playerLoadDate').html(month+'/'+day+'/'+year+' '+hour+':'+minutes+' '+ampm);
      }).fail(function(xhr, textStatus, error) {
        $('#loadingDialog').modal('hide');
        $('#errorDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
        $('#errorHeader').text('failed to load players!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to load players!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });
    });
  
    //Edit Players
    $('#editPlayersButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/getallplayers/', context).done(function(data) {
        var players = data.players;
        var playerRows = '';
        $.each(players, function(i, item) {
          var playerRow = '<div class="list-group-item editPlayersListItem" style="padding:0px 0px 0px 0px;" id="editPlayersListItem" data-name="'+item.name+'" data-club-member-number="'+item.club_member_number+'">';
          playerRow += '  <div class="row">';
          playerRow += '    <div class="col-sm-1"></div>';
          playerRow += '      <div class="col-sm-10">';
          playerRow += '        <div class="input-group">';
          playerRow += '          <div class="input-group-btn">';
          playerRow += '            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Action <span class="caret"></span></button>';
          playerRow += '            <ul class="dropdown-menu">';
          playerRow += '              <li><a href="#">Activate</a></li>';
          playerRow += '              <li><a href="#">Inactivate</a></li>';
          playerRow += '              <li><a href="#">View Player Page</a></li>';
          playerRow += '            <li role="separator" class="divider"></li>';
          playerRow += '              <li><a href="#">Delete</a></li>';
          playerRow += '            </ul>';
          playerRow += '         </div>';
          playerRow += '	    <input id="editPlayersClubMemberNumber" type="text" class="form-control input-group-addon editPlayersClubMemberNumber" style="text-align:right;background-color:#fff;" value="'+item.club_member_number+'" data-original-value="'+item.club_member_number+'" />';
          playerRow += '     	    <span class="input-group-btn" style="width:0px;"></span>';
          playerRow += '	    <input id="editPlayersName" type="text" class="form-control input-group-addon editPlayersName" style="text-align:left;background-color:#fff;" value="'+item.name+'" data-original-value="'+item.name+'" />';
          playerRow += '   	    <span class="input-group-btn" style="width:0px;"></span>';
          playerRow += '	    <input id="editPlayersHandicapIndex" type="text" class="form-control input-group-addon editPlayersHandicapIndex" style="text-align:right;background-color:#fff;" value="'+item.handicap_index+'" data-original-value="'+item.handicap_index+'" />';
          playerRow += '       </div>';
          playerRow += '    </div>';
          playerRow += '    <div class="col-sm-1"></div>';
          playerRow += '  </div>';
          playerRow += '</div>';
          playerRows += playerRow;
        });
        $('#editPlayersList').html(playerRows);
        $('#editPlayers').modal({backdrop: 'static'}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to get all players!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to get all players!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#loadingDialog').modal('hide');
      });
    });
  	function updateEditPlayersList() {
  		$('.editPlayersListItem').show();
    	var currentQuery = $('#editPlayersSearchInput').val().toUpperCase();
    	if (currentQuery !== '') {
      	$('.editPlayersListItem').each(function(index) {
      	  var currentKeyword = $(this).find('.editPlayersName').val().toUpperCase();
      	  var currentKeywordOriginal = $(this).find('.editPlayersName').data('originalValue').toUpperCase();
        	if (currentKeyword.indexOf(currentQuery) === -1) {
        		$(this).hide();
        	} else {
          	if (currentKeywordOriginal.indexOf(currentQuery) === -1) {
          		$(this).hide();
          	}
        	}
      	});
    	}
  	}
    $('#editPlayersSearchInput').keyup(function(event){
      updateEditPlayersList();
  	});
    $('#newPlayerButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {
        clubMemberNumber: $('#newPlayerclubMemberNumber').val(),
        name: $('#newPlayerName').val(),
        handicapIndex: $('#newPlayerHandicapIndex').val(),
      };
      $.post('/golf/newplayer/', context).done(function(data) {
        context = {};
        $.post('/golf/getallplayers/', context).done(function(data) {
          var players = data.players;
          var playerRows = '';
          $.each(players, function(i, item) {
            var playerRow = '<div class="list-group-item editPlayersListItem" style="padding:0px 0px 0px 0px;" id="editPlayersListItem" data-name="'+item.name+'" data-club-member-number="'+item.club_member_number+'">';
            playerRow += '  <div class="row">';
            playerRow += '    <div class="col-sm-1"></div>';
            playerRow += '      <div class="col-sm-10">';
            playerRow += '        <div class="input-group">';
            playerRow += '          <div class="input-group-btn">';
            playerRow += '            <button type="button" class="btn fixed-width-btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Action <span class="caret"></span></button>';
            playerRow += '            <ul class="dropdown-menu">';
            playerRow += '              <li><a href="#">Activate</a></li>';
            playerRow += '              <li><a href="#">Inactivate</a></li>';
            playerRow += '              <li><a href="#">View Player Page</a></li>';
            playerRow += '            <li role="separator" class="divider"></li>';
            playerRow += '              <li><a href="#">Delete</a></li>';
            playerRow += '            </ul>';
            playerRow += '         </div>';
            playerRow += '	    <input id="editPlayersClubMemberNumber" type="text" class="form-control input-group-addon editPlayersClubMemberNumber" style="text-align:right;background-color:#fff;" value="'+item.club_member_number+'" data-original-value="'+item.club_member_number+'" />';
            playerRow += '     	    <span class="input-group-btn" style="width:0px;"></span>';
            playerRow += '	    <input id="editPlayersName" type="text" class="form-control input-group-addon editPlayersName" style="text-align:left;background-color:#fff;" value="'+item.name+'" data-original-value="'+item.name+'" />';
            playerRow += '   	    <span class="input-group-btn" style="width:0px;"></span>';
            playerRow += '	    <input id="editPlayersHandicapIndex" type="text" class="form-control input-group-addon editPlayersHandicapIndex" style="text-align:right;background-color:#fff;" value="'+item.handicap_index+'" data-original-value="'+item.handicap_index+'" />';
            playerRow += '       </div>';
            playerRow += '    </div>';
            playerRow += '    <div class="col-sm-1"></div>';
            playerRow += '  </div>';
            playerRow += '</div>';
            playerRows += playerRow;
          });
          $('#editPlayersList').html(playerRows);
        }).fail(function(xhr, textStatus, error) {
          $('#errorDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
          $('#errorHeader').text('failed to get all players!');
          $('#errorText').text(xhr.responseText);
          console.log('failed to get all players!');
          console.log(xhr.responseText);
          console.log(textStatus);
          console.log(error);
        }).always(function(event) {
          $('#loadingDialog').modal('hide');
        });
      }).fail(function(xhr, textStatus, error) {
        $('#errorDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
        $('#errorHeader').text('failed to add a new player!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to add a new player!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      }).always(function(event) {
        $('#loadingDialog').modal('hide');
      });
    });
  
    //Edit Courses
    $('#editCoursesButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/getallcourses/', context).done(function(data) {
        var courses = data.courses;
        var courseRows = '';
        $.each(courses, function(i, item) {
          var courseRow = '<div class="list-group-item editCoursesListItem" style="padding:0px 0px 0px 0px;" id="editCoursesListItem" data-name="'+item.name+'">';
          courseRow += '  <div class="row">';
          courseRow += '    <div class="col-sm-1"></div>';
          courseRow += '    <div class="col-sm-10">';
          courseRow += '      <div class="input-group">';
          courseRow += '        <div class="input-group-btn">';
          courseRow += '          <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Action <span class="caret"></span></button>';
          courseRow += '          <ul class="dropdown-menu">';
          courseRow += '            <li><a href="#">Edit course tees</a></li>';
          courseRow += '            <li role="separator" class="divider"></li>';
          courseRow += '            <li><a href="#">Delete</a></li>';
          courseRow += '          </ul>';
          courseRow += '        </div>';
          courseRow += '        <input id="editCoursesPriority" type="text" class="form-control input-group-addon editCoursesPriority" size="1" style="text-align:left;background-color:#fff;" value="'+item.priority+'" data-original-value="'+item.priority+'" />';
          courseRow += '        <span class="input-group-btn" style="width:0px;"></span>';
          courseRow += '        <input id="editCoursesName" type="text" class="form-control input-group-addon editCoursesName" style="text-align:left;background-color:#fff;" value="'+item.name+'" data-original-value="'+item.name+'" />';
          courseRow += '      </div>';
          courseRow += '    </div>';
          courseRow += '    <div class="col-sm-1"></div>';
          courseRow += '  </div>';
          courseRow += '</div>';
          courseRows += courseRow;
        });
        $('#editCoursesList').html(courseRows);
        $('#editCourses').modal({backdrop: 'static'}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to get all courses!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to get all courses!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#loadingDialog').modal('hide');
      });
    });
  	function updateEditCoursesList() {
  		$('.editCoursesListItem').show();
    	var currentQuery = $('#editCoursesSearchInput').val().toUpperCase();
    	if (currentQuery !== '') {
      	$('.editCoursesListItem').each(function(index) {
      	  var currentKeyword = $(this).find('.editCoursesName').val().toUpperCase();
      	  var currentKeywordOriginal = $(this).find('.editCoursesName').data('originalValue').toUpperCase();
        	if (currentKeyword.indexOf(currentQuery) === -1) {
        		$(this).hide();
        	} else {
          	if (currentKeywordOriginal.indexOf(currentQuery) === -1) {
          		$(this).hide();
          	}
        	}
      	});
    	}
  	}
    $('#editCoursesSearchInput').keyup(function(event) {
      updateEditCoursesList();
  	});
    $('#newCourseButton').click(function(event) {
      
    });
  
    //Print Indexes Signup Sheets
    var option = '<option value="0">------------------------------------------------------</option>';
    $('#clubPrintoutsCourse1').append(option);
    $('#clubPrintoutsCourse2').append(option);
    $.each(courseTees, function(i, item) {
      option = '<option value="'+item.id+'">'+item.course__name+' - '+item.name+'</option>';
      $('#clubPrintoutsCourse1').append(option);
      $('#clubPrintoutsCourse2').append(option);
    });
    $('#clubprintoutsButton').click(function(event) {
      var cr = $('#clubPrintoutsRosterCount').val();
      var c1 = $('#clubPrintoutsCourse1').val();
      var c2 = $('#clubPrintoutsCourse2').val();
      var su = $('#clubPrintoutsSignupCount').val();
      var ss = $('#clubPrintoutsStarterCount').val();
      var pc = $('#clubPrintoutsProximityCount').val();
      var nm = $('#clubPrintoutsNewMembersCount').val();
      var mp = $('#clubPrintoutsMatchPlayCount').val();
      var mpb = $('#clubPrintoutsMatchPlayBuyIn').val();
      var mpc = $('#clubPrintoutsMatchPlayersCount').val();
      window.open('/golf/clubprintouts/?cr='+cr+'&c1='+c1+'&c2='+c2+'&su='+su+'&ss='+ss+'&pc='+pc+'&nm='+nm+'&mp='+mp+'&mpb='+mpb+'&mpc='+mpc);
    });

    //Import/Export/Backup
    $('#exportCourses').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var course = $('#importExportCourse').val();
      var courseId = $('#importExportCourses').find('[value="'+course+'"]').data('value');
      var a = document.createElement('A');
      a.href = '/golf/exportcourse/'+courseId;
      a.download = course+'.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      $('#loadingDialog').modal('hide');
    });
    $('#exportLoadPlayersPlugins').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var loadPlayersPlugin = $('#importExportLoadPlayersPlugin').val();
      var loadPlayersPluginId = $('#importExportLoadPlayersPlugins').find('[value="'+loadPlayersPlugin+'"]').data('value');
      var a = document.createElement('A');
      a.href = '/golf/exportloadplayersplugin/'+loadPlayersPluginId;
      a.download = loadPlayersPlugin+'.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      $('#loadingDialog').modal('hide');
    });
    $('#importExportBackupButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/getimportexportbackupdata/', context).done(function(data) {
        var importExportBackupData = data.importExportBackupData;
        console.log(importExportBackupData);
        $('#importExportDatabaseStatus').val(importExportBackupData.databaseSize);
        $('#importExportCourses').empty();
        $('#importExportCourse').val('');
        $.each(importExportBackupData.courses, function(i, item) {
          var option = '<option data-value="'+item.id+'" value="'+item.name+'"></option>';
          $('#importExportCourses').append(option);
        });
        $('#importExportTournamentRoundImportPlugins').empty();
        $('#importExportTournamentRoundImportPlugin').val('');
        $.each(importExportBackupData.roundImportPlugins, function(i, item) {
          var option = '<option data-value="'+item.id+'" value="'+item.name+'"></option>';
          $('#importExportTournamentRoundImportPlugins').append(option);
        });
        $('#importExportLoadPlayersPlugins').empty();
        $('#importExportLoadPlayersPlugin').val('');
        $.each(importExportBackupData.playerPlugins, function(i, item) {
          var option = '<option data-value="'+item.id+'" value="'+item.name+'"></option>';
          $('#importExportLoadPlayersPlugins').append(option);
        });
        $('#importExportTournamentFormats').empty();
        $('#importExportTournamentFormat').val('');
        $.each(importExportBackupData.formatPlugins, function(i, item) {
          var option = '<option data-value="'+item.id+'" value="'+item.name+'"></option>';
          $('#importExportTournamentFormats').append(option);
        });
        $('#importExportBackup').modal({backdrop: 'static'}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#errorHeader').text('failed to get import/export data!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to get import/export data!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#errorDialog').modal({}).show();
      }).always(function(a, textStatus, b) {
        $('#loadingDialog').modal('hide');
      });
    });
  
    //Settings
    $('#settingsContent').html($('#settingsClubContent').html());
    $('#settingsClubTab').click(function(event) {
      $('#settingsContent').html($('#settingsClubContent').html());
    });
    $('#settingsPluginsTab').click(function(event) {
      $('#settingsContent').html($('#settingsPluginsContent').html());
    });
    $('#settingsCoursesTab').click(function(event) {
      $('#settingsContent').html($('#settingsCoursesContent').html());
    });
    $('#settingsCourseTeesTab').click(function(event) {
      $('#settingsContent').html($('#settingsCourseTeesContent').html());
    });
    $('#settingsButton').click(function(event) {
      $('#settings').modal({backdrop: 'static'}, event.target).show();
    });
    $('#storeSettingsButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      var context = {};
      $.post('/golf/storesettings/', context).done(function(data) {
        $('#loadingDialog').modal('hide');
        $('#settings').modal('hide');
        var d = new Date();
        $('#settingsLoadDate').html(d.toDateString());
      }).fail(function(xhr, textStatus, error) {
        $('#loadingDialog').modal('hide');
        $('#settings').modal('hide');
        $('#errorDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
        $('#errorHeader').text('failed to store settings!');
        $('#errorText').text(xhr.responseText);
        console.log('failed to store settings!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });
    });
  
    //jquery controls
    $('#newTournamentCoursesMS').multiSelect( {
      selectableHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the courses played">',
      selectionHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the courses played">',
      keepOrder: true,
      afterInit: function(ms){
        var that = this,
        $selectableSearch = that.$selectableUl.prev(),
        $selectionSearch = that.$selectionUl.prev(),
        selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
        selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';
        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
        .on('keydown', function(event) {
          if (event.which === 40) {
            that.$selectableUl.focus();
            return false;
          }
        });
        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
        .on('keydown', function(event) {
          if (event.which == 40) {
            that.$selectionUl.focus();
            return false;
          }
        });
      },
      afterSelect: function(values) {
        this.qs1.cache();
        this.qs2.cache();
        var valueId = parseInt(values[0], 10);
        newTournamentCoursesSelectedCourseList.push(newTournamentCoursesAvailableCourseList.filter(function(element) { return element.id === valueId})[0]);
        newTournamentCoursesAvailableCourseList = newTournamentCoursesAvailableCourseList.filter(function(element) { return element.id !== valueId });
      },
      afterDeselect: function(values) {
        this.qs1.cache();
        this.qs2.cache();
        var valueId = parseInt(values[0], 10);
        newTournamentCoursesAvailableCourseList.push(newTournamentCoursesSelectedCourseList.filter(function(element) { return element.id === valueId })[0]);
        newTournamentCoursesSelectedCourseList = newTournamentCoursesSelectedCourseList.filter(function(element) { return element.id !== valueId });
      }
    });
    $('#newTournamentCourseTeesMS').multiSelect( {
      selectableHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the tees played">',
      selectionHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the tees played">',
      keepOrder: true,
      afterInit: function(ms){
        var that = this,
          $selectableSearch = that.$selectableUl.prev(),
          $selectionSearch = that.$selectionUl.prev(),
          selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
          selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';
  
        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
        .on('keydown', function(event) {
          if (event.which === 40) {
            that.$selectableUl.focus();
            return false;
          }
        });
  
        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
        .on('keydown', function(event) {
          if (event.which == 40) {
            that.$selectionUl.focus();
            return false;
          }
        });
      },
      afterSelect: function(values) {
        this.qs1.cache();
        this.qs2.cache();
        var valueId = parseInt(values[0], 10);
        newTournamentCourseTeesSelectedCourseTeeList.push(newTournamentCourseTeesAvailableCourseTeeList.filter(function(element) { return element.id === valueId})[0]);
        newTournamentCourseTeesAvailableCourseTeeList = newTournamentCourseTeesAvailableCourseTeeList.filter(function(element) { return element.id !== valueId });
      },
      afterDeselect: function(values) {
        this.qs1.cache();
        this.qs2.cache();
        var valueId = parseInt(values[0], 10);
        newTournamentCourseTeesAvailableCourseTeeList.push(newTournamentCourseTeesSelectedCourseTeeList.filter(function(element) { return element.id === valueId })[0]);
        newTournamentCourseTeesSelectedCourseTeeList = newTournamentCourseTeesSelectedCourseTeeList.filter(function(element) { return element.id !== valueId });
      }
    });
    $('#editTournamentSearchStartDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#editTournamentSearchFinishDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#editTournamentUploadTournamentRoundDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#settingsClubTees').multiSelect( {
      selectableHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the default club tees">',
      selectionHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the default club tees">',
      keepOrder: true,
      afterInit: function(ms) {
        var that = this,
          $selectableSearch = that.$selectableUl.prev(),
          $selectionSearch = that.$selectionUl.prev(),
          selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
          selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';
  
        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
        .on('keydown', function(event) {
          if (event.which === 40) {
            that.$selectableUl.focus();
            return false;
          }
        });
  
        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
        .on('keydown', function(event) {
          if (event.which == 40) {
            that.$selectionUl.focus();
            return false;
          }
        });
      },
      afterSelect: function(value) {
        this.qs1.cache();
        this.qs2.cache();
        settingsCourseTeeList.push(parseInt(value[0], 10));
        console.log(settingsCourseTeeList);
      },
      afterDeselect: function(value) {
        this.qs1.cache();
        this.qs2.cache();
        settingsCourseTeeList = settingsCourseTeeList.filter(function(element) { return element !== parseInt(value[0], 10) });
        console.log(settingsCourseTeeList);
      }
    });
    $("#importCourses").click(function() {
      $.FileDialog({multiple: true, dropheight: 290, title: 'Import Course(s)'}).on('files.bs.filedialog', function(ev) {
        var files = ev.files;
        var text = "";
        files.forEach(function(f) {
          text += f.name + "<br/>";
        });
        console.log(text);
      }).on('cancel.bs.filedialog', function(ev) {
        console.log("Cancelled!");
      });
    });
    $("#importTournamentRoundImportPlugins").click(function() {
      $.FileDialog({multiple: true, dropheight: 290, title: 'Import Tournament Round Import Plugin(s)'}).on('files.bs.filedialog', function(ev) {
        var files = ev.files;
        var text = "";
        files.forEach(function(f) {
          text += f.name + "<br/>";
        });
        console.log(text);
      }).on('cancel.bs.filedialog', function(ev) {
        console.log("Cancelled!");
      });
    });
    $("#importLoadPlayersPlugins").click(function() {
      $.FileDialog({multiple: true, dropheight: 290, title: 'Import Load Player Plugin(s)'}).on('files.bs.filedialog', function(ev) {
        var files = ev.files;
        var text = "";
        files.forEach(function(f) {
          text += f.name + "<br/>";
        });
        console.log(text);
      }).on('cancel.bs.filedialog', function(ev) {
        console.log("Cancelled!");
      });
    });
    $("#importTournamentFormatPlugins").click(function() {
      $.FileDialog({multiple: true, dropheight: 290, title: 'Import Tournament Format Plugin(s)'}).on('files.bs.filedialog', function(ev) {
        var files = ev.files;
        var text = "";
        files.forEach(function(f) {
          text += f.name + "<br/>";
        });
        console.log(text);
      }).on('cancel.bs.filedialog', function(ev) {
        console.log("Cancelled!");
      });
    });
    $("#importDatabase").click(function() {
      $.FileDialog({multiple: true, dropheight: 290, title: 'Import Database'}).on('files.bs.filedialog', function(ev) {
        var files = ev.files;
        var text = "";
        files.forEach(function(f) {
          text += f.name + "<br/>";
        });
        console.log(text);
      }).on('cancel.bs.filedialog', function(ev) {
        console.log("Cancelled!");
      });
    });
    $('#settingsClubCourses').multiSelect( {
      selectableHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the default club courses">',
      selectionHeader: '<input type="text" class="form-control search-input" autocomplete="off" placeholder="Select the default club courses">',
      keepOrder: true,
      afterInit: function(ms) {
        var that = this,
          $selectableSearch = that.$selectableUl.prev(),
          $selectionSearch = that.$selectionUl.prev(),
          selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
          selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';
  
        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
        .on('keydown', function(event) {
          if (event.which === 40) {
            that.$selectableUl.focus();
            return false;
          }
        });
  
        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
        .on('keydown', function(event) {
          if (event.which == 40) {
            that.$selectionUl.focus();
            return false;
          }
        });
      },
      afterSelect: function(value) {
        this.qs1.cache();
        this.qs2.cache();
        settingsCourseList.push(parseInt(value[0], 10));
        console.log(settingsCourseList);
      },
      afterDeselect: function(value) {
        this.qs1.cache();
        this.qs2.cache();
        settingsCourseList = settingsCourseList.filter(function(element) { return element !== parseInt(value[0], 10) });
        console.log(settingsCourseList);
      }
    });
  });