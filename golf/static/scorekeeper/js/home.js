/* global $, formatsJSON, coursesJSON, courseTeesJSON */
  var newTournamentPage2AvailableCourseList = [];
  var newTournamentPage2SelectedCourseList = [];
  var newTournamentPage3AvailableCourseTeeList = [];
  var newTournamentPage3SelectedCourseTeeList = [];
  $(document).ready(function() {

    //Menu buttons
    //New Tournament
    $('#newTournamentButton').click(function(event) {
      $('#newTournamentPage1Format').empty();
      $.each(formatsJSON, function (i, item) {
        var option = '<option value="' + item.id + '">' + item.name + '</option>';
        $('#newTournamentPage1Format').append(option);
      });
      $('#newTournamentPage1').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#newTournamentPage1SetCoursesButton').click(function(event) {
      $('#newTournamentPage2Courses').multiSelect('refresh');
      newTournamentPage2SelectedCourseList = [];
      newTournamentPage2AvailableCourseList = coursesJSON;
      $.each(coursesJSON, function (i, item) {
        if (item.default) {
          $('#newTournamentPage2Courses').multiSelect('addOption', { value: item.id, text: item.name });
          $('#newTournamentPage2Courses').multiSelect('select', item.id.toString());
        } else {
          $('#newTournamentPage2Courses').multiSelect('addOption', { value: item.id, text: item.name });
        }
      });
      $('#newTournamentPage1').modal('hide');
      $('#newTournamentPage2').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#newTournamentPage2BackButton').click(function(event) {
      $('#newTournamentPage2').modal('hide');
      $('#newTournamentPage1').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#newTournamentPage2SetCourseTeesButton').click(function(event) {
      $('#newTournamentPage3CourseTees').multiSelect('refresh');
      newTournamentPage3SelectedCourseTeeList = [];
      newTournamentPage3AvailableCourseTeeList = courseTeesJSON.filter(function(element) {
        var add = $.each(newTournamentPage2SelectedCourseList, function(i, course) {
          if (course.id === element.course) {
            return false;
          }
          return true;
        });
        return add;
      });
      $.each(newTournamentPage3AvailableCourseTeeList, function (i, item) {
        if (item.default) {
          $('#newTournamentPage3CourseTees').multiSelect('addOption', { value: item.id, text: item.course__name+' - '+item.name });
          $('#newTournamentPage3CourseTees').multiSelect('select', item.id.toString());
        } else {
          $('#newTournamentPage3CourseTees').multiSelect('addOption', { value: item.id, text: item.course__name+' - '+item.name });
        }
      });
      $('#newTournamentPage2').modal('hide');
      $('#newTournamentPage3').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#newTournamentPage3BackButton').click(function(event) {
      $('#newTournamentPage3').modal('hide');
      $('#newTournamentPage2').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#newTournamentPage3startTournamentButton').click(function(event) {
      var context = {
        tournamentName: $('#newTournamentPage1Name').val(),
        dateStart: $('#newTournamentPage1DateStart').val(),
        formatId: $('#newTournamentPage1Format').val(),
        setupId: $('#newTournamentPage1Setup').val(),
        numRounds: $('#newTournamentPage1NumRounds').val(),
        coursesJSON: JSON.stringify(newTournamentPage2SelectedCourseList),
        courseTeesJSON: JSON.stringify(newTournamentPage3SelectedCourseTeeList)
      };
      console.log(context);
      $.redirect('/golf/newtournament/', context, 'POST', '', true);
    });

    //Edit Tournament
    $('#editTournamentButton').click(function(event) {
      $('#editTournament').modal({backdrop: 'static', keyboard: false}, event.target).show();
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
      $('#editPlayers').modal({backdrop: 'static', keyboard: false}, event.target).show();
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
      $('#editCourses').modal({backdrop: 'static', keyboard: false}, event.target).show();
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
      $('#recentActivity').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    //Import/Export/Backup
    $('#importExportBackupButton').click(function(event) {
      $('#importExportBackup').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    //Settings
    $('#settingsButton').click(function(event) {
      $('#settings').modal({backdrop: 'static', keyboard: false}, event.target).show();
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
    $('#newTournamentPage1DateStartDatePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#newTournamentPage2Courses').multiSelect( {
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
        newTournamentPage2SelectedCourseList.push(newTournamentPage2AvailableCourseList.filter(function(element) { return element.id === valueId})[0]);
        newTournamentPage2AvailableCourseList = newTournamentPage2AvailableCourseList.filter(function(element) { return element.id !== valueId });
      },
      afterDeselect: function(values) {
        this.qs1.cache();
        this.qs2.cache();
        var valueId = parseInt(values[0], 10);
        newTournamentPage2AvailableCourseList.push(newTournamentPage2SelectedCourseList.filter(function(element) { return element.id === valueId })[0]);
        newTournamentPage2SelectedCourseList = newTournamentPage2SelectedCourseList.filter(function(element) { return element.id !== valueId });
      }
    });
    $('#newTournamentPage3CourseTees').multiSelect( {
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
        newTournamentPage3SelectedCourseTeeList.push(newTournamentPage3AvailableCourseTeeList.filter(function(element) { return element.id === valueId})[0]);
        newTournamentPage3AvailableCourseTeeList = newTournamentPage3AvailableCourseTeeList.filter(function(element) { return element.id !== valueId });
      },
      afterDeselect: function(values) {
        this.qs1.cache();
        this.qs2.cache();
        var valueId = parseInt(values[0], 10);
        newTournamentPage3AvailableCourseTeeList.push(newTournamentPage3SelectedCourseTeeList.filter(function(element) { return element.id === valueId })[0]);
        newTournamentPage3SelectedCourseTeeList = newTournamentPage3SelectedCourseTeeList.filter(function(element) { return element.id !== valueId });
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