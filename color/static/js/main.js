var $ = jQuery.noConflict();

$(document).ready(function(){
    $('#paths').on("click", function() {
        if($(this).hasClass('paths')){
            $('#path').css({ fill: "#0000003b" });
            $(this).removeClass('paths')
        }else{
            console.log($('.wish').attr('data-id'))
            $.ajax({
                url:$('.wish').attr('data-href'),
                data:{
                    'data_id': $('.wish').attr('data-id'),
                    'csrfmiddlewaretoken' : $('input[name="csrfmiddlewaretoken"]').val(),
                },
                type:'POST',
                dataType: 'json',
                success: function (res, status) {
                    if (res['status'] == 'ok') {
                        $(this).addClass('paths')
                        $('#path').css({ fill: "#EF465A" });
                    }
                },
                error: function (res) {
                    console.log(res.status);
                }
            })
            
        }
    });
    $('.add-cart').on('click', function(params){
        params.preventDefault();
        console.log($(this).attr('href'));
        $.ajax({
            url:$(this).attr('href'),
            data:{
                'data_id': $(this).attr('data-id'),
                'csrfmiddlewaretoken' : $('input[name="csrfmiddlewaretoken"]').val(),
            },
            type:'POST',
            dataType: 'json',
            success: function (res, status) {
                if (res['status'] == 'ok') {
                    $(this).addClass('disabled');
                    document.querySelector('.add-cart').textContent = 'Added to Cart';
                    $(this).addClass('disabled');
                }
            },
            error: function (res) {
                console.log(res.status);
            }
        })
    });
( jQuery ) });