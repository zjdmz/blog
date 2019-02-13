// 检查两次密码是否一致
$(function () {

    var btn_submit = $("#btn-pwd");

    btn_submit.click(function () {
        var new_pwd1 = $("#new_pwd1").val();
        var new_pwd2 = $("#new_pwd2").val();
        var old_pwd = $("#old_pwd").val();
        if (old_pwd.length < 8) {
            console.log(old_pwd);
            window.messageBox.showInfo('旧密码至少是8位哦')
            console.log(old_pwd)
        } else if (new_pwd1.length < 8) {
            window.messageBox.showError('新密码太短，至少8位')
        } else if (new_pwd1 !== new_pwd2) {
            window.messageBox.showInfo('新密码不一致，请核查')
        } else {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                }
            });
            $.ajax({
                //几个参数需要注意一下
                type: "POST",//方法类型
                dataType: "json",//预期服务器返回的数据类型
                url: "/update_password",
                data: $('.edit_pwd_form').serialize(),
                success: function (result) {
                    console.log(typeof (result));//打印服务端返回的数据(调试用)
                    if (result.code === 200) {
                        window.location = "/";
                    } else {
                        window.messageBox.showError(result["message"])
                    }
                },
                error: function () {
                    alert("异常！");
                }
            });
        }
    });
});
