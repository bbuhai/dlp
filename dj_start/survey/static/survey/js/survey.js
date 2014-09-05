(function($){
    $(document).ready(function(){
        var alternative_path = $('#alternative'),
            url = alternative_path.attr('data-url')
            loader = $('#loader');


        var compute = function() {
            $.ajax({
                url: url,
                method: 'GET',
                success: function(xhr) {
                    loader.hide();
                    console.log(xhr);
                    alternative_path.html(xhr);
                },
                error: function(xhr) {
                    console.log(xhr);
                }
            })
        };

        setTimeout(compute, 1500)
        
    });
}(jQuery))