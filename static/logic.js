
$(document).ready(function() {
    $('.accordion').click(function() {
        var $panel = $(this).next('.panel');

        // Check if the next panel is open or not
        if ($panel.css('max-height') !== '0px') {
            $panel.css('max-height', '0px');
        } else {
            // Set max-height to the panel's scrollHeight plus a little extra space
            $panel.css('max-height', $panel.prop('scrollHeight') + 'px');
        }
        
        // Optionally, toggle the 'active' class to highlight the accordion header
        $(this).toggleClass('active');
    });


    
});

