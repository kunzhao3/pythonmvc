$('#submit').click(function() {
    username = $('#username').val();
    password = $('#password').val();
    $.ajax({
        type: 'POST',
        url: '/content/login/login',
        contentType: 'application/json',
        data: JSON.stringify({'username':username,'password':password}),
        dataType: "json",
        success: function (response) {
            if(response.code == 200){
                window.location.href = response.data.redirect_url;
            } else {
                const msg = response.msg;
                $("#myModal").show().append(msg);
                setTimeout(function(){ // 设置定时器，在延迟后执行关闭操作
                    $("#myModal").hide().empty(); // 隐藏模态框
                }, 600); // 设置延迟时间（毫秒）
            }
        },
        error: function (xhr, status, error) {
            // 登录失败后的处理
            console.error(xhr.responseText);
        },
    });
});