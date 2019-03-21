$('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like/', {category_id: catid}, function(data){
        $('#like_count').html(data);
            $('#likes').hide();
    });
});

$('#likes_item').click(function(){
    var adid;
    adid = $(this).attr("data-adid");
    $.get('/rango/like_ad/', {ad_id: adid}, function(data){
        $('#like_count_item').html(data);
            $('#likes_item').hide();
    });
});

$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/rango/suggest/', {suggestion: query}, function(data){
            $('#cats').html(data);
    });
});