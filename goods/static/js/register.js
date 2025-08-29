// 注册表单验证
document.getElementById('register').addEventListener('click', function(e) {
    const username = $('#username').val();
    const password = $('#password').val();
    const confirmPassword = $('#confirm_password').val();
    if (password !== confirmPassword) {
        $("#myModal").show().append('两次输入的密码不一致，请重新输入！');
        setTimeout(function(){ // 设置定时器，在延迟后执行关闭操作
            $("#myModal").hide().empty(); // 隐藏模态框
        }, 600); // 设置延迟时间（毫秒）
        document.getElementById('confirm_password').focus();
    } else {
        $.ajax({
            type: 'POST',
            url: '/content/register/register',
            contentType: 'application/json',
            data: JSON.stringify({'username':username,'password':password}),
            dataType: "json",
            success: function (response) {
                if(response.code == 200){
                    window.location.href = response.data.redirect_url;
                } else {
                    const msg = response.msg;
                    $("#myModal").show().append(msg);
                }
            },
            error: function (xhr, status, error) {
                // 登录失败后的处理
                console.error(xhr.responseText);
            },
        });
    }
});
