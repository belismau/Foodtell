$(document).ready(function(){
  var register = $('.register');
  var login = $('.login');

  register.on('click', function(){
    $('.login').fadeOut('slow').css('display', 'none');
  });

  login.on('click', function(){
    $('.sign-up').fadeOut('slow').css('display', 'none');
  });
});
