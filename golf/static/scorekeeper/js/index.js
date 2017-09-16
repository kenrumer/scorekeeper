/* global $, newTournamentCourseList, newTournamentCourseTeeList, settingsCourseList, settingsCourseTeeList */
  $(document).ready(function() {

    //Menu buttons
    //New Tournament
    $('#newTournamentButton').click(function(event) {
      $('#newTournament').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#startTournamentButton').click(function(event) {
      var context = {
        name: $('#newTournamentName').val(),
        dateStart: $('#newTournamentDateStart').val(),
        format: $('#newTournamentFormat').val(),
        numRounds: $('#newTournamentNumRounds').val(),
        courses: newTournamentCourseList,
        tees: newTournamentCourseTeeList
      };
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
        	if (current_keyword.indexOf(current_query) >=0) {
        		$(this).show();
        	}
      	});
    	} else {
    		$('.editTournamentList #editTournamentListItem').show();
    	}
  	});
    $('#loadTournamentButton').click(function(event){
      window.location.href = '/golf/edittournament/0';
    });

    //Load Players
    $('#loadPlayersButton').click(function(event) {
      $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      $.post('/golf/loadplayers/', {}).done(function(data) {
        var d = new Date();
        $('#loadingDialog').modal('hide');
        $('#playerLoadDate').html(d.toDateString());
      }).fail(function(xhr, textStatus, error) {
        $('#loadingDialog').modal('hide');
        alert('failed to load players: '+xhr.responseText);
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
      	$('.editPlayersList #editPlayersListItem').hide();
      	$('.editPlayersList #editPlayersListItem').each(function() {
        	var current_keyword = $(this).data('name').toUpperCase();
        	if (current_keyword.indexOf(current_query) >=0) {
        		$(this).show();
        	}
      	});
    	} else {
    		$('.editPlayersList #editPlayersListItem').show();
    	}
  	});
    $('#newPlayerButton').click(function(event) {
      $('#enterNewPlayer').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    //Edit Courses
    $('#editCoursesButton').click(function(event) {
      $('#editCourses').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#editCoursesSearchInput').keyup(function(event){
    	var current_query = $('#editCoursesSearchInput').val().toUpperCase();
    	if (current_query !== '') {
      	$('.editCoursesList #editCoursesListItem').hide();
      	$('.editCoursesList #editCoursesListItem').each(function() {
        	var current_keyword = $(this).data('name').toUpperCase();
        	if (current_keyword.indexOf(current_query) >=0) {
        		$(this).show();
        	}
      	});
    	} else {
    		$('.editCoursesList #editCoursesListItem').show();
    	}
  	});
    $('#newCourseButton').click(function(event) {
      $('#enterNewCourseName').modal({backdrop: 'static', keyboard: false}, event.target).show();
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

    //Settings
    $('#settingsButton').click(function(event) {
      $('#settings').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#storeSettingsButton').click(function(event) {
      $.post('/golf/storesettings/', {}).done(function(data) {
        $('#loadingDialog').modal('hide');
        $('#settings').modal('hide');
        var d = new Date();
        $('#settingsLoadDate').html(d.toDateString());
        $('#loadingDialog').modal({backdrop: 'static', keyboard: false}, event.target).show();
      }).fail(function(xhr, textStatus, error) {
        $('#loadingDialog').modal('hide');
        $('#settings').modal('hide');
        alert('failed to store settings: '+xhr.responseText);
        console.log('failed to store settings!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });
    });

    //jquery controls
    $('#newTournamentDateStartDatePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#editTournamentSearchStartDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#editTournamentSearchEndDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#newTournamentCourses').multiSelect( {
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
      afterSelect: function(value) {
        this.qs1.cache();
        this.qs2.cache();
        newTournamentCourseList.push(parseInt(value[0], 10));
        console.log(newTournamentCourseList);
      },
      afterDeselect: function(value) {
        this.qs1.cache();
        this.qs2.cache();
        newTournamentCourseList = newTournamentCourseList.filter(function(element) { return element !== parseInt(value[0], 10) });
        console.log(newTournamentCourseList);
      }
    });
    $('#newTournamentTees').multiSelect( {
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
      afterSelect: function(value){
        this.qs1.cache();
        this.qs2.cache();
        newTournamentCourseTeeList.push(parseInt(value[0], 10));
        console.log(newTournamentCourseTeeList);
      },
      afterDeselect: function(value){
        this.qs1.cache();
        this.qs2.cache();
        newTournamentCourseTeeList = newTournamentCourseTeeList.filter(function(element) { return element !== parseInt(value[0], 10) });
        console.log(newTournamentCourseTeeList);
      }
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
  });
