function get_title_by_url(url){
    return $.ajax(url);
}
function handle_url(event){
    get_title_by_url(event.currentTarget.value)
        .then(function(html){
            var title = $(html).filter('title').text();
            set_title(title);
        });
}
function set_title(title){
    $('#title').val(title);
}
$(function(){
    $('#url').change(handle_url);
});