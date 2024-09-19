$(".wrap_title").each( function(index){
    let elem = $(this);
    let panel = elem.next(".wrap_panel");
    let button = elem.children(".wrap_button");

    elem.click(function(){
        if(panel.is(":visible")){
            button.text("⯈");
            panel.slideUp();
        }
        else{
            button.text("⯆");
            panel.slideDown();
        }
    })
});