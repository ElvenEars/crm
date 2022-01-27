
$('.toggle').click(function(e) {
    e.preventDefault();

  var $this = $(this);

  if ($this.next().hasClass('show')) {
      $this.next().removeClass('show');
      $this.next().slideUp(350);
  } else {
      $this.parent().parent().find('li .inner').removeClass('show');
      $this.parent().parent().find('li .inner').slideUp(350);
      $this.next().toggleClass('show');
      $this.next().slideToggle(350);
  }
});

$('.product-count').change(function(e){
    e.preventDefault();
    if( $(this).val() > 0){
        $(this).parents('li').toggleClass('product-checked')
    }
    else{
        $(this).parents('li').removeClass('product-checked')
    }
});
$('li.product').on("click",function(e){
    $(this).children().find('.product-count').focus();
}) // дописать

$('.show-more').click(function(e){
    if($(this).parent().find('li.list-more').hasClass('show') ){
        $(this).parent().find('li.list-more').removeClass('show');
        $(this).text('Свернуть');
    }
    else {
        $(this).parent().find('li.list-more').toggleClass('show');
        $(this).text('Развернуть');
    }
})
