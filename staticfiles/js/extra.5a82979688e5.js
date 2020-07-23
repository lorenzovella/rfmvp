$(document).ready(function () {
  $('.control-group').last().css('margin-bottom','180px');
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
});
