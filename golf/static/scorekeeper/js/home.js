/* global $, clubsJSON, coursesJSON, courseTeesJSON, tournamentsJSON, tournamentRoundsJSON, formatPluginsJSON, playersJSON, playerPluginsJSON, activitiesJSON, moment */
  var newTournamentCoursesAvailableCourseList = [];
  var newTournamentCoursesSelectedCourseList = [];
  var newTournamentCourseTeesAvailableCourseTeeList = [];
  var newTournamentCourseTeesSelectedCourseTeeList = [];
  $(document).ready(function() {

  //Menu buttons
  //New Tournament Wizard
  $('#newTournamentButton').click(function(event) {
    $('#newTournamentName').val(clubsJSON[0].default_tournament_name+' - '+moment().format('MM/DD/YYYY'));
    $('#newTournamentRoundCount').val(1);
    $('#newTournament').modal({backdrop: 'static'}, event.target).show();
  });

  $('#newTournamentNextButton').click(function(event) {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    var context = {
      tournamentName: $('#newTournamentName').val()
    };
    $.post('/golf/checkfortournamentduplicate/', context).done(function(data) {
      console.log(data);
      $('#loadingDialog').modal('hide');
      var duplicate = data.duplicate;
      if (duplicate == true) {
        $('#newTournamentDuplicate').modal({backdrop: 'static', keyboard: false}, event.target).show();
      } else {
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
          $.each(formatPluginsJSON, function (i, item) {
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
      }
    }).fail(function(xhr, textStatus, error) {
      $('#newTournament').modal('hide');
      $('#loadingDialog').modal('hide');
      $('#errorDialog').modal({}).show();
      $('#errorHeader').text('failed to determine if this is a duplicate tournament!');
      $('#errorText').text(xhr.responseText);
      console.log('failed to load players!');
      console.log(xhr.responseText);
      console.log(textStatus);
      console.log(error);
    });
  });

  $('#newTournamentDuplicateCancelTournament').click(function(event) {
    $('#newTournamentDuplicate').modal('hide');
    $('#newTournament').modal('hide');
  });
  $('#newTournamentDuplicateCreateNewTournament').click(function(event) {
    $('#newTournamentDuplicate').modal('hide');
    $('#newTournament').modal('hide');
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
      $.each(formatPluginsJSON, function (i, item) {
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
  });

  $('#newTournamentRoundsBackButton').click(function(event) {
    $('#newTournamentRounds').modal('hide');
    $('#newTournament').modal({backdrop: 'static'}, event.target).show();
  });
  $('#newTournamentRoundsNextButton').click(function(event) {
    $('#newTournamentRounds').modal('hide');
    $('#newTournamentCoursesMS').multiSelect('refresh');
    newTournamentCoursesSelectedCourseList = [];
    newTournamentCoursesAvailableCourseList = coursesJSON;
    $.each(coursesJSON, function (i, item) {
      if (item.default) {
        $('#newTournamentCoursesMS').multiSelect('addOption', { value: item.id, text: item.name });
        $('#newTournamentCoursesMS').multiSelect('select', item.id.toString());
      } else {
        $('#newTournamentCoursesMS').multiSelect('addOption', { value: item.id, text: item.name });
      }
    });
    $('#newTournamentCourses').modal({backdrop: 'static'}, event.target).show();
  });

  $('#newTournamentCoursesBackButton').click(function(event) {
    $('#newTournamentCourses').modal('hide');
    $('#newTournamentRounds').modal({backdrop: 'static'}, event.target).show();
  });
  $('#newTournamentCoursesNextButton').click(function(event) {
    $('#newTournamentCourses').modal('hide');
    $('#newTournamentCourseTeesMS').multiSelect('refresh');
    newTournamentCourseTeesSelectedCourseTeeList = [];
    newTournamentCourseTeesAvailableCourseTeeList = courseTeesJSON.filter(function(element) {
      var add = false;
      $.each(newTournamentCoursesSelectedCourseList, function(i, course) {
        if (course.id === element.course__id) {
          add = true;
          return false;
        }
      });
      return add;
    });
    $.each(newTournamentCourseTeesAvailableCourseTeeList, function (i, item) {
      if (item.default) {
        $('#newTournamentCourseTeesMS').multiSelect('addOption', { value: item.id, text: item.course__name+' - '+item.name });
        $('#newTournamentCourseTeesMS').multiSelect('select', item.id.toString());
      } else {
        $('#newTournamentCourseTeesMS').multiSelect('addOption', { value: item.id, text: item.course__name+' - '+item.name });
      }
    });
    $('#newTournamentCourseTees').modal({backdrop: 'static'}, event.target).show();
  });

  $('#newTournamentCourseTeesBackButton').click(function(event) {
    $('#newTournamentCourseTees').modal('hide');
    $('#newTournamentCourses').modal({backdrop: 'static'}, event.target).show();
  });
  $('#newTournamentCourseTeesNextButton').click(function(event) {
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
      roundCount: roundCount,
      tournamentRoundsJSON: JSON.stringify(tournamentRounds),
      availableCoursesJSON: JSON.stringify(newTournamentCoursesSelectedCourseList),
      availableCourseTeesJSON: JSON.stringify(newTournamentCourseTeesSelectedCourseTeeList)
    };
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    $.post('/golf/newtournament/', context).done(function(data) {
      $('#loadingDialog').modal('hide');
      $.redirect('/golf/tournament/', data, 'POST', '', true);
    }).fail(function(xhr, textStatus, error) {
      $('#loadingDialog').modal('hide');
      $('#errorDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      $('#errorHeader').text('failed to create a tournament!');
      $('#errorText').text(xhr.responseText);
      console.log('failed to create a tournament!');
      console.log(xhr.responseText);
      console.log(textStatus);
      console.log(error);
    });
  });

  //Edit Tournament
  $('#editTournamentButton').click(function(event) {
    $('#editTournament').modal({backdrop: 'static'}, event.target).show();
  });
  $('#editTournamentSearchInput').keyup(function(event){
  	var current_query = $('#editTournamentSearchInput').val().toUpperCase();
  	if (current_query !== '') {
    	$('.editTournamentList #editTournamentListItem').hide();
    	$('.editTournamentList #editTournamentListItem').each(function(){
      	var current_keyword = $(this).text().toUpperCase();
      	if (current_keyword.indexOf(current_query) >= 0) {
      		$(this).show();
      	}
    	});
  	} else {
  		$('.editTournamentList #editTournamentListItem').show();
  	}
	});
  $('#saveTournamentsButton').click(function(event){
    window.location.href = '/golf/edittournament/0';
  });

  //Load Players
  $('#loadPlayersButton').click(function(event) {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    $.post('/golf/loadplayers/', {}).done(function(data) {
      $('#loadingDialog').modal('hide');
      var d = new Date();
      $('#playerLoadDate').html(d.toDateString());
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
    $('#editPlayers').modal({backdrop: 'static'}, event.target).show();
  });
  $('#editPlayersSearchInput').keyup(function(event){
  	var current_query = $('#editPlayersSearchInput').val().toUpperCase();
  	if (current_query !== '') {
    	$('#editPlayersListItem').hide();
    	$('#editPlayersListItem').each(function() {
      	var current_keyword = $(this).data('name').toUpperCase();
      	if (current_keyword.indexOf(current_query) >= 0) {
      		$(this).show();
      	}
    	});
  	} else {
  		$('#editPlayersListItem').show();
  	}
	});
  $('#newPlayerButton').click(function(event) {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    $.post('/golf/newplayer/', context).done(function(data) {
      $('#loadingDialog').modal('hide');
    }).fail(function(xhr, textStatus, error) {
      $('#loadingDialog').modal('hide');
      $('#errorDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      $('#errorHeader').text('failed to add a new player!');
      $('#errorText').text(xhr.responseText);
      console.log('failed to store settings!');
      console.log(xhr.responseText);
      console.log(textStatus);
      console.log(error);
    });
  });

  //Edit Courses
  $('#editCoursesButton').click(function(event) {
    $('#editCourses').modal({backdrop: 'static'}, event.target).show();
  });
  $('#editCoursesSearchInput').keyup(function(event){
  	var current_query = $('#editCoursesSearchInput').val().toUpperCase();
  	if (current_query !== '') {
    	$('#editCoursesListItem').hide();
    	$('#editCoursesListItem').each(function() {
      	var current_keyword = $(this).data('name').toUpperCase();
      	if (current_keyword.indexOf(current_query) >= 0) {
      		$(this).show();
      	}
    	});
  	} else {
  		$('#editCoursesListItem').show();
  	}
	});
  $('#newCourseButton').click(function(event) {
    
  });

  //Print Indexes
  $('#printIndexesButton').click(function(event) {
    window.open('/golf/printplayers/');
  });

  //Print Signup Sheets
  $('#signupSheetsButton').click(function(event) {
    window.open('/golf/printsignupsheets/');
  });

  //Recent Activity
  $('#recentActivityButton').click(function(event) {
    $('#recentActivity').modal({backdrop: 'static'}, event.target).show();
  });

  //Import/Export/Backup
  $('#importExportBackupButton').click(function(event) {
    $('#importExportBackup').modal({backdrop: 'static'}, event.target).show();
  });

  //Settings
  $('#settingsButton').click(function(event) {
    $('#settings').modal({backdrop: 'static'}, event.target).show();
  });
  $('#storeSettingsButton').click(function(event) {
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    $.post('/golf/storesettings/', {}).done(function(data) {
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
  $('#editTournamentSearchEndDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
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
  $("#importClubScores").click(function() {
    $.FileDialog({multiple: true, dropheight: 290, title: 'Import Club Score(s)'}).on('files.bs.filedialog', function(ev) {
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
  $("#importClubTypes").click(function() {
    $.FileDialog({multiple: true, dropheight: 290, title: 'Import Club Type(s)'}).on('files.bs.filedialog', function(ev) {
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
  $("#importFormats").click(function() {
    $.FileDialog({multiple: true, dropheight: 290, title: 'Import Format(s)'}).on('files.bs.filedialog', function(ev) {
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