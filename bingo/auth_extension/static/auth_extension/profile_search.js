$(document).ready(function() {
    $('#suggestion').keyup(function() {
        var query = $(this).val();
        console.log(query)
         $.get('/profile/suggest/', {suggestion: query}, function(data){
             $('#profile-list').html(data);
         });
    });
});
