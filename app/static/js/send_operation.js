$(document).ready(function()) {
  $('form').on('submit', function(event) {
    $.ajax({
      data : {
        
      },
      type : 'POST',
      url : '/session_cmd',
    })
    .done(function(data) {});

    event.preventDefault();

  });
};
