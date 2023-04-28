$(window).load(function() {
    equalHeight($("left-col, right-col"));

     //equalize function
     function equalHeight(group) {
        tallest = 0;
        group.each(function() {
            thisHeight = $(this).height();
            if(thisHeight > tallest) {
                tallest = thisHeight;
            }
        });
        group.height(tallest);
    }
}); 