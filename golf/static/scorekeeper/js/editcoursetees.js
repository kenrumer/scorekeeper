  /* global $, courseTees, courseId */
  var table;
  var removeId = -1;
  
  function rowHasChanged(row) {
    for (var i = 0; i < row.cells.length; i++) {
      var child = row.cells[i].children[0];
      if (child.type === 'checkbox') {
        if (String(child.checked) != child.getAttribute('data-original-value')) {
          row.classList.add('highlight');
          return true;
        }
      } else if (child.type === 'number') {
        if (String(child.value) != child.getAttribute('data-original-value')) {
          row.classList.add('highlight');
          return true;
        }
      } else {
        if (child.value != child.getAttribute('data-original-value')) {
          row.classList.add('highlight');
          return true;
        }
      }
    }
    return false;
  }
  
  function valueChange(data) {
    var table1 = document.getElementById('editCourseTeesTable');
    if ((data.type === 'checkbox') && (data.getAttribute('data-checkbox-type') === 'only-one')) {
      if (event.stopPropagation) {
        event.stopPropagation();
      } else {
        window.event.cancelBubble = true;
      }
      if (!data.checked) {
        data.checked = false;
      } else {
        for (var j = 1; j < table1.rows.length; j++) {
          var row = table1.rows[j];
          var child = row.cells[0].children[0];
          child.checked = false;
        }
        data.checked = true;
      }
    }
    for (var j = 1; j < table1.rows.length; j++) {
      var row = table1.rows[j];
      var id = row.getAttribute('id');
      if (id > 0) {
        if (rowHasChanged(row)) {
          row.classList.add('highlight');
        } else {
          row.classList.remove('highlight');
        }
      } else {
        row.classList.add('highlight');
      }
    }
  }
  
  function updateCourseTee(data) {
    var id = data.getAttribute('data-id');
    var row = document.getElementById(id);
    if (rowHasChanged(row)) {
      var courseId = data.getAttribute('data-course-id');
      var isDefault = row.cells[0].children[0].checked;
      var priority = row.cells[1].children[0].value;
      var name = row.cells[2].children[0].value;
      var slope = row.cells[3].children[0].value;
      var color = row.cells[4].children[0].value;
      var context = { 'default': isDefault, 'priority': priority, 'name': name, 'slope': slope, 'color': color};
      $.post('/golf/updatecoursetee/'+courseId+'/'+id, context).done(function(data) {
        row.classList.remove('highlight');
      }).fail(function(xhr, textStatus, error) {
        alert('failed to create course tee: '+xhr.responseText);
        console.log('failed to create course tee!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });
    }
  }
  
  function createCourseTee(data) {
    console.log(data);
    var id = data.getAttribute('data-id');
    var courseId = data.getAttribute('data-course-id');
    var row = document.getElementById(id);
    var isDefault = row.cells[0].children[0].checked;
    var priority = row.cells[1].children[0].value;
    var name = row.cells[2].children[0].value;
    var slope = row.cells[3].children[0].value;
    var color = row.cells[4].children[0].value;
    var actions = row.cells[5];
    var context = { 'default': isDefault, 'priority': priority, 'name': name, 'slope': slope, 'color': color};
    console.log(context);
    $.post('/golf/createcoursetee/'+courseId, context).done(function(data) {
      var id = data.data[0].id;
      row.classList.remove('highlight');
      row.setAttribute('id', id);
      actions.innderHTML = ' \
        <div class="dropdown"> \
          <button class="btn btn-default dropdown-toggle editcoursesActionsMenu" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"> \
            &#9733 \
            <span class="caret"></span> \
          </button> \
          <ul class="dropdown-menu" aria-labelledby="dropdownMenu1"> \
            <li><a href="/golf/editcourseteeholes/'+courseId+'/'+id+'">Edit Tee Holes</a></li> \
            <li><a href="#" onclick="updateCourseTee(this);" data-id="'+id+'" data-course-id="'+courseId+'">Update Course Tee</a></li> \
            <li><a href="#" data-action="removeCourseTee" data-id="'+id+'">Remove Course Tee</a></li> \
          </ul> \
        </div>';
    }).fail(function(xhr, textStatus, error) {
      alert('failed to create course tee: '+xhr.responseText);
      console.log('failed to create course tee!');                                                                                                                                                          
      console.log(xhr.responseText);
      console.log(textStatus);
      console.log(error);
    });
  }
  
  function removeCourseTee(data) {
    var id = data.getAttribute('data-id');
    $.get('/golf/removecoursetee/'+id).done(function() {
      $('#remove-course-tee').modal('hide');
      table.row('#'+id).remove().draw();
    }).fail(function() {
      $('#remove-course-tee-error').text();
    });
  }
  
  function removeCreatedCourseTee(data) {
    var id = data.getAttribute('data-id');
    table.row('#'+id).remove().draw();
  }
  
  $(document).ready(function() {
  
    $('#removeCourseTeeButton').click(function(event) {
      var id = $(this).attr('data-id');
      $.get('/golf/removecoursetee/'+id).done(function() {
        $('#removeCourseTee').modal('hide');
        table.row('#'+id).remove().draw();
      }).fail(function() {
        $('#removeCourseTeeError').text();
      });
    });

    $('#removeCourseTee').on('show.bs.modal', function(event) {
      var $button = $(event.relatedTarget);
      var id = $button.attr('data-id');
      var row = document.getElementById(id);
      var name = row.cells[2].children[0].value;
      $('#removeCourseTeeButton').attr('data-id', id);
      $('#removeCourseTeeName').text(name);
    });

    $('#courseTeeDefault').on('change', function(event) {
      valueChange(this);
    });
    $('#courseTeePriority').on('input', function(event) {
      valueChange(this);
    });
    $('#courseTeeName').on('input', function(event) {
      valueChange(this);
    });
    $('#courseTeeSlope').on('input', function(event) {
      valueChange(this);
    });
    $('#courseTeeColor').on('input', function(event) {
      valueChange(this);
    });

    table = $('#editCourseTeesTable').DataTable({
      'dom': 'Bfrtip',
      'buttons': [{
        'text': '<u>A</u>dd Course Tee',
        'key': {
          'key': 'a',
          'shiftKey': true
        },
        'action': function ( event, dt, node, config ) {
          var rowNode = dt.row.add({'id': removeId, 'priority': -1, 'default': false, 'name': '', 'slope': 113, 'color': 0}).draw().node();
          $(rowNode).addClass('highlight');
          removeId--;
        }
      }],
      'scrollY': '75vh',
      'scrollCollapse': false,
      'paging': false,
      'data': courseTees,
      'columnDefs': [{
        'targets': 0,
        'createdCell': function (td, cellData, rowData, row, col) {
          if (cellData) {
            $(td).html('<input id="courseTeeDefault" type="checkbox" data-checkbox-type="only-one" data-id="'+rowData['id']+'" data-original-value=true checked=true>');
          } else {
            $(td).html('<input id="courseTeeDefault" type="checkbox" data-checkbox-type="only-one" data-id="'+rowData['id']+'" data-original-value=false>');
          }
        },
        'orderable': true
      }, {
        'targets': 1,
        'createdCell': function (td, cellData, rowData, row, col) {
          $(td).html('<input id="courseTeePriority" type="number" min="-1" max="99" value="'+cellData+'" data-id='+rowData['id']+' data-original-value="'+cellData+'">');
        },
        'orderable': true
      }, {
        'targets': 2,
        'createdCell': function (td, cellData, rowData, row, col) {
          $(td).html('<input id="courseTeeName" type="text" value="'+cellData+'" size="80px" data-id='+rowData['id']+' data-original-value="'+cellData+'">');
        },
        'orderable': false
      }, {
        'targets': 3,
        'createdCell': function (td, cellData, rowData, row, col) {
          $(td).html('<input id="courseTeeSlope" type="number" value="'+cellData+'" min=0 max=999>');
        },
        'orderable': false
      }, {
        'targets': 4,
        'createdCell': function (td, cellData, rowData, row, col) {
          var options = '';
          var colors = ['None', 'Yellow', 'Green', 'Red', 'White', 'Blue', 'Black', 'Gold'];
          for (var i = 0; i < colors.length; i++) {
            if (i == cellData) {
              options = options+'<option value="'+i+'" selected>'+colors[i]+'</option>';
            } else {
              options = options+'<option value="'+i+'">'+colors[i]+'</option>';
            }
          }
          $(td).html('<select id="courseTeeColor" data-id='+rowData['id']+' data-original-value="'+cellData+'">'+options+'</select>');
        },
        'orderable': false
      }, {
        'targets': 5,
        'createdCell': function (td, cellData, rowData, row, col) {
          var $cell = $(td);
          if (rowData.id < 0) {
            $cell.html(' \
              <div class="dropdown"> \
                <button class="btn btn-default dropdown-toggle editCoursesActionsMenu" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"> \
                  &#9733 \
                  <span class="caret"></span> \
                </button> \
                <ul class="dropdown-menu" aria-labelledby="dropdownMenu1"> \
                  <li><a href="#" onclick="createCourseTee(this);" data-id="'+rowData.id+'" data-course-id="'+courseId+'">Create Course Tee</a></li> \
                  <li><a href="#" onclick="removeCreatedCourseTee(this);" data-id="'+rowData.id+'">Remove Course Tee</a></li> \
                </ul> \
              </div>');
          } else {
            $cell.html(' \
              <div class="dropdown"> \
                <button class="btn btn-default dropdown-toggle editcoursesActionsMenu" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"> \
                  &#9733 \
                  <span class="caret"></span> \
                </button> \
                <ul class="dropdown-menu" aria-labelledby="dropdownMenu1"> \
                  <li><a href="/golf/editcourseteeholes/'+courseId+'/'+rowData.id+'">Edit Tee Holes</a></li> \
                  <li><a href="#" onclick="updateCourseTee(this);" data-id="'+rowData.id+'" data-course-id="'+courseId+'">Update Course Tee</a></li> \
                  <li><a href="#" data-action="removeCourseTee" data-id="'+rowData.id+'">Remove Course Tee</a></li> \
                </ul> \
              </div>');
          }
        },
        'orderable': false
      } ],
      'columns': [
        { 'data': 'default' },
        { 'data': 'priority' },
        { 'data': 'name' },
        { 'data': 'slope' },
        { 'data': 'color' },
        { 'data': null }
      ],
      'order': [[ 1, 'desc' ]],
      'rowId': 'id',
      'drawCallback': function(settings) {
        $('[data-action="removeCourseTee"]').click(function(event) {
          event.stopPropagation();
          $('#removeCourseTee').modal({}, event.target).show();
        });
      },
      'processing': true,
      'language': {
        'processing': '<p class="bg-warning">Processing...</p>'
      }
    });
  });