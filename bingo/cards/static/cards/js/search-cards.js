$(document).ready(function() {
    $('#suggestion').keyup(function() {
        var query = $(this).val();
        console.log(query)
         $.get('/cards/suggest/', {suggestion: query}, function(data){
             $('#cards').html(data);
         });
    });
});
