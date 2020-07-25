$(document).ready(function () {

// Responsiveness helpers
  $('.control-group').last().css('margin-bottom','180px');

  let fullWindowHeight = window.innerHeight;
  let keyboardIsProbablyOpen = false;

  window.addEventListener("resize", function() {
    if(window.innerHeight == fullWindowHeight) {
      $('.footer').show()
      keyboardIsProbablyOpen = false;
    } else if(window.innerHeight < fullWindowHeight*0.9) {
      $('.footer').hide()
      keyboardIsProbablyOpen = true;
    }
  });

  $(document).keypress(
  function(event){
    if (event.which == '13') {
      event.preventDefault();
      $('.btn-next').trigger('click');
      return false;
    }
  });
});
