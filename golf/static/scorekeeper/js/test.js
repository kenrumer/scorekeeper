
  $(document).ready(function() {
    $('#testButton').click(function(event) {
      var context = {
      };
      $.post('/golf/testview/', context).done(function(data) {
        console.log(data);
        $('#testOutput').text(data);
      }).fail(function(xhr, textStatus, error) {
        console.log('failed to get the test data!');
        console.log(xhr.responseText);
        console.log(textStatus);
        console.log(error);
      });
    });
  });