function accountmanager() {
  alert("It's not how much money you make, but how much money you invest, how hard it works for you, and how many generations you keep it for. - Elite Tesla Traders Firm");
};


$(window).scroll(function() {
  $(".slideanimation").each(function(){
  var pos = $(this).offset().top;

  var winTop = $(window).scrollTop();
  if (pos < winTop + 600) {
    $(this).addClass("sliderider");
  }
  });
});

$(window).scroll(function() {
  $(".slideanim").each(function(){
  var pos = $(this).offset().top;

  var winTop = $(window).scrollTop();
  if (pos < winTop + 600) {
    $(this).addClass("slider");
  }
  });
});

$('.counter-count').each(function () {
  $(this).prop('Counter',0).animate({
      Counter: $(this).text()
  }, {
      duration: 11000,
      easing: 'swing',
      step: function (now) {
          $(this).text(Math.ceil(now));
      }
  });
});