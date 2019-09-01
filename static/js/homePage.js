

function bSearch() {
    var text = $('#s-text').val();
    
    $.ajax({
        url:'/search?t=1',
        type:'get',
        headers:{
            'X-CSRFtoken':$.cookie('csrftoken'),
        },
        data:{
            'text':text
        },
        dataType:'json',
        success:function () {

        }
    })
}