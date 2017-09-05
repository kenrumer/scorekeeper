/* global $ */
  $(document).ready(function() {

    //Menu buttons
    $('#newTournamentButton').click(function(event) {
      $('#newTournament').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#startTournamentButton').click(function(event) {
      var context = {
        name: $('#newTournamentName').val(),
        dateStart: $('#newTournamentDateStart').val(),
        format: $('#newTournamentFormat').val(),
        numRounds: $('#newTournamentNumRounds').val(),
        courses: $('#newTournamentCourses').val(),
        tees: $('#newTournamentTees').val()
      };
      $.redirect('/golf/newtournament/', context, 'POST', '', true);
    });

    $('#editTournamentButton').click(function(event) {
      $('#editTournament').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#editTournamentSearchInput').keyup(function(event){
    	var current_query = $('#editTournamentSearchInput').val();
    	if (current_query !== '') {
      	$('.editTournamentList li').hide();
      	$('.editTournamentList li').each(function(){
        	var current_keyword = $(this).text();
        	if (current_keyword.indexOf(current_query) >=0) {
        		$(this).show();
        	}
      	});
    	} else {
    		$('.editTournamentList li').show();
    	}
  	});
    $('#loadTournamentButton').click(function(event){
      window.location.href = '/golf/edittournament/0';
    });

    $('#loadPlayersButton').click(function(event) {
      $('#playersLoading').css('visibility', 'visible');
      $.post('/golf/loadplayers/', {}).done(function(data) {
        var d = new Date();
        $('#playerLoadDate').html(d.toDateString());
        $('#playersLoading').css('visibility', 'hidden');
      }).fail(function(xhr, textStatus, error) {
        alert('failed to load players: '+xhr.responseText);
        console.log('failed to load players!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#playersLoading').css('visibility', 'hidden');
      });
    });
    
    $('#editPlayersButton').click(function(event) {
      $('#editPlayers').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#editPlayersSearchInput').keyup(function(event){
    	var current_query = $('#editPlayersSearchInput').val();
    	if (current_query !== '') {
      	$('.editPlayersList li').hide();
      	$('.editPlayersList li').each(function(){
        	var current_keyword = $(this).text();
        	if (current_keyword.indexOf(current_query) >=0) {
        		$(this).show();
        	}
      	});
    	} else {
    		$('.editPlayersList li').show();
    	}
  	});

    $('#printIndexesButton').click(function(event) {
      window.open('/golf/printplayers/');
    });

    $('#signupSheetsButton').click(function(event) {
      window.open('/golf/printsignupsheets/');
    });

    $('#importExportBackupButton').click(function(event) {
      $('#importExportBackup').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    $('#editCoursesButton').click(function(event) {
      $('#editCourses').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#editCoursesSearchInput').keyup(function(event){
    	var current_query = $('#editCoursesSearchInput').val();
    	if (current_query !== '') {
      	$('.editCoursesList li').hide();
      	$('.editCoursesList li').each(function(){
        	var current_keyword = $(this).text();
        	if (current_keyword.indexOf(current_query) >=0) {
        		$(this).show();
        	}
      	});
    	} else {
    		$('.editCoursesList li').show();
    	}
  	});
    $('#newCourseButton').click(function(event) {
      $('#enterNewCourseName').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });

    $('#settingsButton').click(function(event) {
      $('#settings').modal({backdrop: 'static', keyboard: false}, event.target).show();
    });
    $('#storeSettingsButton').click(function(event) {
      $('#settings').modal('hide');
      $.post('/golf/storesettings/', {}).done(function(data) {
        var d = new Date();
        $('#settingsLoadDate').html(d.toDateString());
        $('#settingsLoading').css('visibility', 'hidden');
      }).fail(function(xhr, textStatus, error) {
        alert('failed to store settings: '+xhr.responseText);
        console.log('failed to store settings!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
        $('#settingsLoading').css('visibility', 'hidden');
      });
    });

    //jquery controls
    $('#newTournamentDateStartDatePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#editTournamentSearchStartDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#editTournamentSearchEndDateDateTimePicker').datetimepicker({format: 'MM/DD/YYYY'});
    $('#newTournamentCourses').multiSelect( {
      selectableHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the courses played">',
      selectionHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the courses played">',
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
      afterSelect: function() {
        this.qs1.cache();
        this.qs2.cache();
      },
      afterDeselect: function() {
        this.qs1.cache();
        this.qs2.cache();
      }
    });
    $('#newTournamentTees').multiSelect( {
      selectableHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the tees played">',
      selectionHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the tees played">',
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
      afterSelect: function(){
        this.qs1.cache();
        this.qs2.cache();
      },
      afterDeselect: function(){
        this.qs1.cache();
        this.qs2.cache();
      }
    });
    $('#settingsClubCourses').multiSelect( {
      selectableHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the default club courses">',
      selectionHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the default club courses">',
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
      afterSelect: function() {
        this.qs1.cache();
        this.qs2.cache();
      },
      afterDeselect: function() {
        this.qs1.cache();
        this.qs2.cache();
      }
    });
    $('#settingsClubTees').multiSelect( {
      selectableHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the default club tees">',
      selectionHeader: '<input type="text" class="search-input" autocomplete="off" placeholder="Select the default club tees">',
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
      afterSelect: function() {
        this.qs1.cache();
        this.qs2.cache();
      },
      afterDeselect: function() {
        this.qs1.cache();
        this.qs2.cache();
      }
    });
  });
