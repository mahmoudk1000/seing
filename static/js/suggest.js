$(document).ready(function() {
    $('#search_url_homepage_id').on('input', function() {
        var query = $(this).val();
        $.get('/autocomplete', {query: query}, function(data) {
            $('#suggestion-list').empty();
            data.forEach(function(suggestion) {
                $('#suggestion-list').append('<li>' + suggestion + '</li>');
            });
        });
    });
});
