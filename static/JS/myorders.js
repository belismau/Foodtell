function sortByOrdnr() {

  var allaOrdnr = document.getElementsByClassName("ordernummer");

  var antal = allaOrdnr.length;

  var listWithAllaOrdnr = [];
  for (var i = 0; i < antal; i++) {
    listWithAllaOrdnr.push(allaOrdnr[i].innerHTML);
  }

  listWithAllaOrdnr.sort(
    function(a, b) {
      return b - a;
    }
  )

  for (var i = 0; i < antal; i++) {
    document.getElementsByClassName("ordernummer")[i].innerHTML = listWithAllaOrdnr[i];

  }

  console.log(listWithAllaOrdnr);

}
