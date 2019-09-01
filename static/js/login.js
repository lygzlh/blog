

function loginSub() {
    var username = $('#username').val();
    var password = $('#password').val();

    $.ajax({
        url:'/login.html',
        headers:{
            'X-CSRFtoken':$.cookie('csrftoken'),
        },
        type:'post',
        data:{
            'username':username,
            'password':password,
        },
        dataType:'json',
        success:function(arg){
            if(arg.state){
                alert('登录成功');
                location.href='/';
            }else {
                alert('用户名或密码错误');
                location.reload();
            }
        }

    })

}