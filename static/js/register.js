

function registerSub() {
    var username = $('#username').val();
    var password = $('#password').val();
    var password1 = $('#password1').val();
    if(password == password1){
        $.ajax({
            url:'/register.html',
            type:'post',
            headers:{
                'X-CSRFtoken':$.cookie('csrftoken'),
            },
            data:{
                'username':username,
                'password':password
            },
            dataType:'json',
            success:function (arg) {
                if(arg.state){
                    alert('注册成功');
                    location.href='/login.html'
                }else {
                    alert(arg.message);
                    location.reload();
                }
            }

        })
    }else {
        alert('两次密码不一样');
    }
}