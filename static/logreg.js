$(document).ready(function(){
  var producent = $('.producentButton');
  var konsument = $('.konsumentButton');
  var divHover = $('.divHover')

  producent.on('click', function(){
    $('.containerKonsument').fadeOut(3).css('display', 'none');
    $('.containerProducent').fadeIn(3);
  });

  konsument.on('click', function(){
    $('.containerProducent').fadeOut(3).css('display', 'none');
    $('.containerKonsument').fadeIn(3);
  });

  konsument.on('click', function(){
    $('.containerProducent').fadeOut(3).css('display', 'none');
    $('.containerKonsument').fadeIn(3);
  });
});

// BUTTON
$(document).ready(function(){
  $(document).on("click",".front",function(){
    var border = $(".back").outerWidth()-$(".back").innerWidth();
    if ($(".front").position().left != 0){
      $(".front").css("left", 0);
      $(".back").css("background-color","lightgreen");
    }else{
      $(".front").css("left",($(".back").outerWidth()-$(".front").outerWidth()) + "px");
      $(".back").css("background-color","lightcoral");
    }
  });
})
