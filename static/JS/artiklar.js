var articleInterval = setInterval(function() {

  var articleElements = document.getElementsByClassName("date");

  for(var i = 0; i < articleElements.length; i++) {

    var articleDate = articleElements[i].innerText;

    var articleTime = articleElements[i].nextElementSibling.innerText;

    var articleTime = articleTime.substr(2);

    var total = articleDate + 'T' + articleTime + ':00';

    var countDownTime = new Date(total).getTime();

    var elAppear = articleElements[i].previousElementSibling.previousElementSibling;

    elAppear.setAttribute('data-countdown', countDownTime);

    var timeNow = new Date().getTime();

    var difference = countDownTime - timeNow;

    var days = Math.floor(difference / (1000 * 60 * 60 * 24));
    var hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((difference % (1000 * 60)) / 1000);

    var result = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

    elAppear.innerText = result;

    if (difference < 100) {
      location.reload();
    }
  }

}, 1000);

// När användaren vill slutföra beställningen

$('.areYouSure').click(function() {
  // Antal kvar i artikeln
  var antalKvar = $(this).closest('div').find('.subtitle').text();
  var antalKvar = antalKvar.substring(7);
  var antalKvarInt = parseInt(antalKvar, 10);

  // Antal användaren valt
  var antalChosen = $(this).closest('form').find('.antalChosen').val();
  var antalChosenInt = parseInt(antalChosen, 10);

  // Se till att man endast kan köpa antalet artiklar som varje artikel visar
  if (antalChosenInt > antalKvarInt || antalChosenInt < 1 || isNaN(antalChosenInt)) {
    $(this).closest('div').find('.noDisplay').css("width", "0");
  } else {
    $(this).closest('div').find('.noDisplay').css("width", "100%");

    var artikelChosen = $(this).closest('div').find('.artikelChosen').text();

    $(this).closest('div').find('.antalDisplay').append(antalChosenInt);
    $(this).closest('div').find('.namnDisplay').append(artikelChosen);
  }
});

$('.back').click(function() {
  $(".noDisplay").css("width", "0");
  $(this).closest('form').find('.antalDisplay').empty();
  $(this).closest('form').find('.namnDisplay').empty();
});
