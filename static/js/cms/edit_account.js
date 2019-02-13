function ajax_post() {

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
        url: "/update",
        data: $('.edit_form').serialize(),
        success: function (result) {
            console.log(typeof (result));//打印服务端返回的数据(调试用)
            window.messageBox.showSuccess(result["message"]);
            setTimeout(
                window.location = "/edit_account", 5000
            )},
        error: function () {
            window.messageBox.showError("异  常！")
        }
    });
}


// 个人中心页面 编辑/取消 按钮功能
$(function () {
    var edit_btn = $("#edit_btn");
    var undo_btn = $(".undo_btn");
    var input_display = $("div").children("input");
    var user_btn = $(".username");
    var captcha = $(".captcha");
    // 编辑按钮
    edit_btn.click(function () {
        for (var i = 1; i < input_display.length; i++) {
            input_display[i].disabled = '';
            input_display[i].style.border = "1px solid deepskyblue";
        }
        captcha.each(function () {
            $(this).removeClass("hidden");
        });
        user_btn.attr("undo", "1");
    });
    // 取消按钮
    undo_btn.click(function () {
        for (var i = 1; i < input_display.length; i++) {
            input_display[i].disabled = 'True';
            input_display[i].style.border = "";
            user_btn.attr("undo", "");
        }
        captcha.each(function () {
            $(this).addClass("hidden")
        });
    });
});

// 个人中心页面 提交 修改个人信息
$(function () {
    var submit_btn = $("#submit_btn");
    var user_btn = $(".username");
    submit_btn.click(function () {
        if (user_btn.attr("undo") === "1") {
            var telephone = $("#telephone").val();
            var email = $("#email").val();  // 邮件验证码
            if (!telephone || telephone.length !== 11) {
                window.messageBox.showError('手机号码不正确！');
            } else if (email.indexOf('@') < 0) {
                console.log(telephone);
                window.messageBox.showError('邮箱不正确')
            } else {
                ajax_post();
            }
        } else {
            window.messageBox.show("请先点击编辑，而后提交！");
        }
    })
});


// 点击发送短信验证码
$(function () {
    var smsBtn = $('.sms_captcha_span');

    function send_sms() {
        // 获取手机号码的时候，获取的是手机号码，而不是手机号码的输入框
        var sms_teltphone = $("#telephone");
        var telephone = sms_teltphone.val();
        if (!telephone || telephone.length !== 11) {
            window.messageBox.showError('手机号码不正确！')
        } else {
            $.get({
                'url': '/sms_captcha',
                dataType: "json",//预期服务器返回的数据类型
                'data': {'telephone': telephone},
                'success': function (result) {
                    console.log(result);
                    if (result["code"] === 'OK') {
                        window.messageBox.showSuccess("验证码发送成功,请注意查收！");
                    } else if (result["code"] === 'repeat') {
                        window.messageBox.showInfo("验证码 5分钟 内有效哦！");
                    } else if (result['code'] === 302) {
                        window.messageBox.showError("手机号码已经注册!");
                    } else {
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


// 点击发送邮件
$(function () {
    var emailBtn = $('.email_captcha'); // 按钮
    function send_email() {
        var email = $("#email").val();
        console.log('email_text %s' % email);
        if ((email.indexOf('@') < 0) && (email.slice(-4) !== '.com')) {
            window.messageBox.showError('邮箱不正确！')
        } else {
            $.get({
                'url': '/send_emails',
                dataType: "json",//预期服务器返回的数据类型
                'data': {'email': email},
                'success': function (result) {
                    console.log(result);
                    window.messageBox.showInfo(result.message);
                    var count = 30;
                    emailBtn.addClass('disabled');
                    emailBtn.unbind('click');
                    var timer = setInterval(function () {
                        emailBtn.text(count + "s");
                        count--;
                        if (count <= 0) {
                            clearInterval(timer);
                            emailBtn.text('发送邮件');
                            emailBtn.removeClass('disabled');
                            emailBtn.click(send_email);
                            console.log('--' * 20)
                        }
                    }, 1000);
                },
                'fail': function (error) {
                    window.messageBox.showError("服务器异常，请稍后再试！")
                }
            });
        }
    }

    emailBtn.click(send_email)
});


