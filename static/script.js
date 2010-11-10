jQuery(function($){
    $('a.vote_up, a.vote_down').live('click', function(){
        var link = $(this).fadeOut();
        $.post(this.href, function(data){
            link.parent()
                .find('span.points')
                .fadeOut(function(){
                    $(this).text(data).fadeIn();
                });
        });
        return false;
    });
});
