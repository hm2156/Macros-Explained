
$(document).ready(function() {
    $('.accordion').click(function() {
        var $panel = $(this).next('.panel');

       
        if ($panel.css('max-height') !== '0px') {
            $panel.css('max-height', '0px');
        } else {
           
            $panel.css('max-height', $panel.prop('scrollHeight') + 'px');
        }
        
     
        $(this).toggleClass('active');
    });


    
});

