// 登录注册页面切换
$(function () {
    var loginclick = $("#login-click");
    var registerclick = $("#register-click");
    var formlogin = $("#form-login");
    var formregister = $("#form-register");
    loginclick.click(function () {
        formregister.addClass("click-hidden");
        registerclick.removeClass("back_ground");
        formlogin.removeClass("click-hidden");
        loginclick.addClass("back_ground");
    });
    registerclick.click(function () {
        formlogin.addClass("click-hidden");
        loginclick.removeClass("back_ground");
        registerclick.addClass("back_ground");
        formregister.removeClass("click-hidden");
    })
});

// 错误消息 2 秒后消失
function message_hide() {
    var message_error = $("#message_error");
    setTimeout(function () {
        message_error.html("");
    }, 2000);
}

$(function () {
    var login_button = $("#login-button");
    login_button.click(
        message_hide()
    )
});


// 点击发送短信验证码
$(function () {
    var smsBtn = $('.sms_captcha_span');

    function send_sms() {
        // 获取手机号码的时候，获取的是手机号码，而不是手机号码的输入框
        var sms_captcha = $("#telephone2");
        var telephone = sms_captcha.val();
        if (!telephone || telephone.length != 11) {
            window.messageBox.showError('手机号码不正确！')
        } else {
            $.get({
                'url': '/sms_captcha',
                dataType: "json",//预期服务器返回的数据类型
                'data': {'telephone': telephone},
                'success': function (result) {
                    if (result["code"] === 'OK') {
                        window.messageBox.showSuccess("验证码发送成功,请注意查收！");
                    } else if (result['code'] === 'repeat') {
                        window.messageBox.showInfo("验证码5分钟内有效哦！");
                    } else if (result['code'] === 'telephone error') {
                        window.messageBox.showError("手机号码不正确！");
                    }
                    else {
                        window.messageBox.showError("验证码发送失败，请稍后再试!");
                    }
                    var count = 30;
                    smsBtn.addClass('disabled');
                    smsBtn.unbind('click');
                    var timer = setInterval(function () {
                        smsBtn.text(count + "s");
                        count--;
                        if (count <= 0) {
                            clearInterval(timer);
                            smsBtn.text('发送验证码');
                            smsBtn.removeClass('disabled');
                            smsBtn.click(send_sms);
                        }
                    }, 1000);
                },
                'fail': function (error) {
                    window.messageBox.showError("服务器异常，请稍后再试！")
                }
            });
        }
    }

    smsBtn.click(send_sms)
});


// ajax提交注册
$(function () {
    var submit = $("#submits1");
    submit.click(function (event) {
        var messages = $("#message_error");
        messages.html = '';
        // event.preventDefault();
        var sms_captcha = $("#telephone2");
        var telephone = sms_captcha.val();
        if (!telephone || telephone.length != 11) {
            window.messageBox.showError('手机号码不正确！')
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
                url: "/register",
                data: $('#form-form').serialize(),
                success: function (result) {
                    console.log(typeof (result));//打印服务端返回的数据(调试用)
                    if (result.code === 200) {
                        window.location = "/";
                    } else {
                        window.messageBox.showError(result["messages"])
                    }
                },
                error: function () {
                    alert("异常！");
                    // window.location = "/register";
                }
            });
        }
    })
});


