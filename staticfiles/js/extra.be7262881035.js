$(document).ready(function () {

  $('.control-group').last().css('margin-bottom','180px');

  if($('#id_cachorro_wizard-current_step').val() == "CachorroForm"){
    var arr = [];
    $.getJSON("/static/racas.json", function(data) {
        $.each(data, function(key, value) {
            if ($.inArray(value.name, arr) === -1) {
                arr.push(value.name)
            }
        })
    });
    $('#id_CachorroForm2-raca').autocomplete({
     source: arr,
     minLength: 2,
    })
    let fullWindowHeight = window.innerHeight;
    let keyboardIsProbablyOpen = false;
  }

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
  $("#optionalText").click(function (){
    $("#optionalForm").show();
    $("#optionalText").hide();
    $("#nextStep").hide();
  })
  $("#nextStep").click(function (){
    $(".btn-next").click();
  })
});
