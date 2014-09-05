var app = app || {};

(function($) {
    app.handle_submit_test = function() {
        var form = $('#pers_test');
        form.submit(function(e){
            /*$.ajax({
                url: form.attr('action'),
                data: form.serialize(),
                type: 'POST',
                complete: function(xhr) {
                    console.log(xhr);
                }
            });
            return false;*/
            return true;
        });
    };

    $(document).ready(function(){
        app.handle_submit_test();
    });
}(jQuery))
