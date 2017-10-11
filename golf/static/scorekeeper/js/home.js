/* global $, clubsJSON, defaultNumRounds, formatsJSON, coursesJSON, courseTeesJSON */
  var newTournamentCoursesAvailableCourseList = [];
  var newTournamentCoursesSelectedCourseList = [];
  var newTournamentCourseTeesAvailableCourseTeeList = [];
  var newTournamentCourseTeesSelectedCourseTeeList = [];
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth() + 1;
  var yyyy = today.getFullYear();
  if (dd < 10) {
    dd = '0' + dd;
  }
  if (mm < 10) {
    mm = '0' + mm;
  }
  var strToday = dd+'/'+mm+'/'+yyyy;
  $(document).ready(function() {

  //Menu buttons
  //New Tournament Wizard
  $('#newTournamentButton').click(function(event) {
    $('#newTournamentFormats').empty();
    $('#newTournamentFormatName').val(clubsJSON[0].default_tournament_name+' - '+strToday);
    $.each(formatsJSON, function (i, item) {
      $('#newTournamentFormats').append('<option value="' + item.id + '">' + item.name + '</option>');
    });
    //This is an option for format because need to know if we are using players or teams in the scorecards
    //  I'm guessing this becomes part of the format plugin
    $('#newTournamentFormatSetup').html('');
    var setupOptions = '<option value="0">Normal</option>';
    setupOptions += '<option value="1">2-man Team</option>';
    setupOptions += '<option value="2">4-man Team</option>';
    $('#newTournamentFormatSetup').append(setupOptions);
    $('#newTournamentFormatNumRounds').val(defaultNumRounds);
    $('#newTournamentFormat').modal({backdrop: 'static'}, event.target).show();
  });
  
  $('#newTournamentFormatNextButton').click(function(event) {
    var duplicate = false;
    $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
    var context = {
      tournamentName: $('#newTournamentFormatName').val()
    };
    $.post('/golf/checkfortournamentduplicate/', context).done(function(data) {
      $('#loadingDialog').modal('hide');
      duplicate = data.duplicate;
      console.log(duplicate);
      /*Pretty much working, but interferes with testing.  This checks if there is a duplicate tournament.*/
      if (duplicate == true) {
        $('#newTournamentDuplicate').modal({backdrop: 'static', keyboard: false}, event.target).show();
      } else {
        $('#newTournamentFormat').modal('hide');
        var numRounds = parseInt($('#newTournamentFormatNumRounds').val(), 10);
        //Show choose dates
        $('#newTournamentDatesRoundsPlaceholder').html('');
        var datesInput = '<div class="list-group newTournamentDatesList">';
        for (var i = 1; i <= numRounds; i++) {
          datesInput += '  <div class="row" id="newTournamentDatesListItem'+i+'">';
         	datesInput += '    <div class="col-sm-3"></div>';
         	datesInput += '    <div class="col-sm-3">';
         	datesInput += '      <input type="text" class="form-control" value="Round '+i+'" disabled />';
          datesInput += '    </div>';
          datesInput += '    <div class="col-sm-3 input-group date" id="newTournamentDatesRoundDatePicker'+i+'">';
          datesInput += '      <input type="text" class="form-control" id="newTournamentDatesDateStart'+i+'" value="'+strToday+'" />';
          datesInput += '      <span class="input-group-addon">';
          datesInput += '        <span class="glyphicon glyphicon-calendar"></span>';
          datesInput += '      </span>';
          datesInput += '    </div>';
         	datesInput += '    <div class="col-sm-3"></div>';
          datesInput += '  </div>';
        }
        datesInput += '</div>';
        $('#newTournamentDatesRoundsPlaceholder').append(datesInput);
        for (var i = 1; i <= numRounds; i++) {
          $('#newTournamentDatesRoundsPlaceholder').find('#newTournamentDatesRoundDatePicker'+i).datetimepicker({format: 'MM/DD/YYYY'});
        }
        $('#newTournamentDates').modal({backdrop: 'static'}, event.target).show();
      }
    }).fail(function(xhr, textStatus, error) {
      $('#newTournamentFormat').modal('hide');
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
    $('#newTournamentFormat').modal('hide');
  });
  $('#newTournamentDuplicateCreateNewTournament').click(function(event) {
    $('#newTournamentDuplicate').modal('hide');
    $('#newTournamentFormat').modal('hide');
    var numRounds = parseInt($('#newTournamentFormatNumRounds').val(), 10);
    //Show choose dates
    $('#newTournamentDatesRoundsPlaceholder').html('');
    var datesInput = '<div class="list-group newTournamentDatesList">';
    for (var i = 1; i <= numRounds; i++) {
      datesInput += '  <div class="row" id="newTournamentDatesListItem'+i+'">';
     	datesInput += '    <div class="col-sm-3"></div>';
     	datesInput += '    <div class="col-sm-3">';
     	datesInput += '      <input type="text" class="form-control" value="Round '+i+'" disabled />';
      datesInput += '    </div>';
      datesInput += '    <div class="col-sm-3 input-group date" id="newTournamentDatesRoundDatePicker'+i+'">';
      datesInput += '      <input type="text" class="form-control" id="newTournamentDatesDateStart'+i+'" value="'+strToday+'" />';
      datesInput += '      <span class="input-group-addon">';
      datesInput += '        <span class="glyphicon glyphicon-calendar"></span>';
      datesInput += '      </span>';
      datesInput += '    </div>';
     	datesInput += '    <div class="col-sm-3"></div>';
      datesInput += '  </div>';
    }
    datesInput += '</div>';
    $('#newTournamentDatesRoundsPlaceholder').append(datesInput);
    for (var i = 1; i <= numRounds; i++) {
      $('#newTournamentDatesRoundsPlaceholder').find('#newTournamentDatesRoundDatePicker'+i).datetimepicker({format: 'MM/DD/YYYY'});
    }
    $('#newTournamentDates').modal({backdrop: 'static'}, event.target).show();
  });

  $('#newTournamentDatesBackButton').click(function(event) {
    $('#newTournamentDates').modal('hide');
    $('#newTournamentFormat').modal({backdrop: 'static'}, event.target).show();
  });
  $('#newTournamentDatesNextButton').click(function(event) {
    $('#newTournamentDates').modal('hide');
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
    $('#newTournamentDates').modal({backdrop: 'static'}, event.target).show();
  });
  $('#newTournamentCoursesNextButton').click(function(event) {
    $('#newTournamentCourses').modal('hide');
    $('#newTournamentCourseTeesMS').multiSelect('refresh');
    newTournamentCourseTeesSelectedCourseTeeList = [];
    newTournamentCourseTeesAvailableCourseTeeList = courseTeesJSON.filter(function(element) {
      var add = $.each(newTournamentCoursesSelectedCourseList, function(i, course) {
        if (course.id === element.course) {
          return false;
        }
        return true;
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
    var numRounds = parseInt($('#newTournamentFormatNumRounds').val(), 10);
    var tournamentDates = [];
    for (var i = 1; i <= numRounds; i++) {
      tournamentDates.push($('#newTournamentDatesDateStart'+i).val());
    }
    var context = {
      tournamentName: $('#newTournamentFormatName').val(),
      tournamentDates: JSON.stringify(tournamentDates),
      formatId: $('#newTournamentFormats').val(),
      setupId: $('#newTournamentFormatSetup').val(),
      numRounds: $('#newTournamentFormatNumRounds').val(),
      coursesJSON: JSON.stringify(newTournamentCoursesSelectedCourseList),
      courseTeesJSON: JSON.stringify(newTournamentCourseTeesSelectedCourseTeeList)
    };
    console.log(context);
    $.redirect('/golf/newtournament/', context, 'POST', '', true);
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