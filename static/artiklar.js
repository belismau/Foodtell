var articleInterval = setInterval(function() {

  // Fångar upp information om artiklens datum

  var articleElements = document.getElementsByClassName("date");

  // Skapar en for-loop pga alla artiklar i min db ska köra denna kod
  // "Kör for-loopen så många gånger som det finns datum i db:n"

  for(var i = 0; i < articleElements.length; i++) {

    // Fångar upp det som finns i articleElements[i] och lagrar det i en variabel

    var articleDate = articleElements[i].innerText;

    // Fångar upp det som finns efter articleElements[i] och lagrar det i en variabel

    var articleTime = articleElements[i].nextElementSibling.innerText;

    // Tar bort mellanrummet som finns i min HTML-kod

    var articleTime = articleTime.substr(2);

    // Lagrar det enligt formatet "1995-12-17T03:24:00" som exempel
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date

    var total = articleDate + 'T' + articleTime + ':00';

    // Omvandlar artikelns information ovan till millisekunder

    var countDownTime = new Date(total).getTime();

    // Fångar upp det element som är föregående x2 från articleElements och lagrar det i en variabel

    var elAppear = articleElements[i].previousElementSibling.previousElementSibling;

    // Återkommer

    elAppear.setAttribute('data-countdown', countDownTime);

    // Ger nuvarande tid

    var timeNow = new Date().getTime();

    // Skillnaden mellan artikelns tid och nuvarande tid
    // Resultatet ges i millisekunder

    var difference = countDownTime - timeNow;

    // Beräknar tiden för dagar, timmar, minuter och sekunder

    var days = Math.floor(difference / (1000 * 60 * 60 * 24));
    var hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((difference % (1000 * 60)) / 1000);

    // Lagrar tiden som skapats ovan tillsammans i en variabel

    var result = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

    elAppear.innerText = result;

    // När countdown är 50 millisekunder

    if (difference < 100) {

      // Uppdaterar sidan

      location.reload();

    }

  }

// Funktionen körs varje 1000 millisekund, därav 1000

}, 1000);
