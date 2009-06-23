$(document).ready(function(){
    if (!$('#username').val()) {
        $('#username').val('username');
    }
    
    if (!$('#password').val()) {
        $('#password').val('examplepassword');
    }
    
    $('#username').one('focus', function(){
        if (this.value == 'username'){
            this.value = '';
        }
    });
    
    $('#password').one('focus', function(){
        if (this.value == 'examplepassword'){
            this.value = '';
        }
    });
    
    $('#next').val(window.location.pathname);
    if ($('#logout').length) {
        $('#logout')[0].href += '?next=' + window.location.pathname;
    }
    
    $('#search').one('focus', function(){
        this.value = '';
    });
});