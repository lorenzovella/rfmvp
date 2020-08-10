$(document).ready(function () {

// Responsiveness helpers
  $('.control-group').last().css('margin-bottom','180px');

  let fullWindowHeight = window.innerHeight;
  let keyboardIsProbablyOpen = false;

  $(document).keypress(
  function(event){
    if (event.which == '13') {
      event.preventDefault();
      $('.btn-next').trigger('click');
      return false;
    }
  });
});
