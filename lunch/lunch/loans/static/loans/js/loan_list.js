(function ($) {
$('.btn-delete').click(function () {
  var button = this;
  $.ajax({
    'url': $(button).data('href'),
    'type': 'DELETE'
  }).done(function () {
    $(button).parent('.loan').remove();
  }).fail(function (e) {
    console.log(e);
  });
});
})(jQuery);