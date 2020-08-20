$(document).ready(function () {
// Responsiveness helpers
  // $('.control-group').last().css('margin-bottom','180px');
  $(document).keypress(
  function(event){
    if (event.which == '13') {
      event.preventDefault();
      $('.btn-next').trigger('click');
      return false;
    }
  });
});
