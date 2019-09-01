

function changePwd() {
    var spwd = $('#sPwd').val();
    if(!spwd){
        alert('原密码不能为空');
        return 0
    }
    var cpwd = $('#cPwd').val();
    if(!cpwd){
        alert('修改密码不能为空');
        return 0
    }
    
    $.ajax({
        url:'/user-center/update-psw.html',
        type:'post',
        headers: {'x-CSRFtoken': $.cookie('csrftoken')},
        data:{
            'spwd':spwd,
            'cpwd':cpwd,
        },
        dataType:"json",
        success:function (arg) {
            if(arg.state){
                alert('修改密码成功,请重新登录');
                location.href = '/login.html';
            }else {
                alert('原密码不正确');
            }
        }
        
    })
}