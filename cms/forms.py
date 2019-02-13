# -*- coding:utf-8 -*-
from .models import User
from django.core.cache import cache

""" 验证表单 """
from django import forms


# 登录
class LoginForm(forms.Form):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={
        "required": "必须输入手机号码",
        "max_length": "手机号码不能超过11位",
        "min_length": "手机号码不能少于11位"})
    # sms_captcha = forms.CharField(min_length=4, max_length=4, error_messages={
    #     "required": "必须输入验证码！",
    #     "min_length": "验证码只能是4位",
    #     "max_length": "验证码只能是4位",
    # })
    password = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入手机号码",
        "min_length": "密码不能少于8位",
        "max_length": "密码不能多于18位"
    })
    remember = forms.IntegerField(required=False)


# 注册
class RegisterForm(forms.Form):
    username1 = forms.CharField(required=False, max_length=100, min_length=4, error_messages={
        "required": "请填写用户名",
        "max_length": "用户名不能超过100个字符！",
        "min_length": "用户名太短！"
    })
    telephone1 = forms.CharField(max_length=11, min_length=11, error_messages={
        "required": '必须填写手机号码',
        "max_length": "手机号码不能超过11位",
        "min_length": "手机号码不能少于11位"
    })
    email1 = forms.EmailField(required=False)
    password1 = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入手机号码",
        "min_length": "密码不能少于8位",
        "max_length": "密码不能多于18位"
    })
    password2 = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入手机号码",
        "min_length": "密码不能少于8位",
        "max_length": "密码不能多于18位"
    })
    img_captcha1 = forms.CharField(min_length=4, max_length=4, error_messages={
        "required": "必须输入验证码！",
        "min_length": "验证码只能是4位",
        "max_length": "验证码只能是4位",
    })
    sms_captcha1 = forms.CharField(min_length=4, max_length=4, error_messages={
        "required": "必须输入验证码！",
        "min_length": "验证码只能是4位",
        "max_length": "验证码只能是4位",
    })
    remember1 = forms.IntegerField(required=False)

    def availed_data(self, request):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password2 != password1:
            self.add_error("password2", "两次密码输入不一致！")
            return False

        img_captcha = cleaned_data.get("img_captcha1")
        server_img_captcha = request.session.get("img_captcha")
        print("img_captcha = ", img_captcha)
        if img_captcha.lower().strip() != server_img_captcha.lower().strip():
            self.add_error("img_captcha", "验证码错误！")
            return False

        telephone = cleaned_data.get("telephone1")
        print("form_telephone = ", telephone)
        if User.objects.filter(telephone=telephone).exists():
            self.add_error("telephone1", "手机号码已注册！%s" % telephone)
            return False

        return True


# 注册2
class RegisterForm2(forms.Form):
    telephone2 = forms.CharField(max_length=11, min_length=11, error_messages={
        "required": '必须填写手机号码',
        "max_length": "手机号码不能超过11位",
        "min_length": "手机号码不能少于11位"
    })

    password1 = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入手机号码",
        "min_length": "密码不能少于8位",
        "max_length": "密码不能多于18位"
    })
    password2 = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入手机号码",
        "min_length": "密码不能少于8位",
        "max_length": "密码不能多于18位"
    })

    sms_captcha2 = forms.CharField(min_length=4, max_length=4, error_messages={
        "required": "必须输入验证码！",
        "min_length": "验证码只能是4位",
        "max_length": "验证码只能是4位",
    })
    remember2 = forms.IntegerField(required=False)

    def availed_data(self):
        cleaned_data = self.cleaned_data
        telephone = cleaned_data.get("telephone2")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        sms_captcha = cleaned_data.get("sms_captcha2")
        if sms_captcha != cache.get(telephone):
            self.add_error("sms_captcha2", "短信验证码不正确！")

        if password2 != password1:
            self.add_error("password2", "两次密码输入不一致！")
            return False

        if User.objects.filter(telephone=telephone).exists():
            self.add_error("telephone2", "手机号码已注册！%s" % telephone)
            return False

        return True


# 修改个人信息
class UpdateForm(forms.Form):
    username = forms.CharField(required=False, max_length=100, min_length=4, error_messages={
        "required": "请填写用户名",
        "max_length": "用户名不能超过100个字符！",
        "min_length": "用户名太短！"
    })
    telephone = forms.CharField(required=True, max_length=11, min_length=11, error_messages={
        "required": '必须填写手机号码',
        "max_length": "手机号码不能超过11位",
        "min_length": "手机号码不能少于11位"
    })
    email = forms.EmailField(required=True, error_messages={"required": "请填写正确的邮箱！"})
    user_id = forms.IntegerField(required=True, error_messages={"required": "用户不存在！"})

    def availed_data(self):
        user_id = self.cleaned_data.get('user_id')
        if not User.objects.filter(pk=user_id).exists():
            self.add_error("user_id", "账户未注册！")
            return False
        return True


# 修改密码
class UpdatePasswordForm(forms.Form):
    user_id = forms.IntegerField()
    old_pwd = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入旧密码",
        "min_length": "密码不能少于6位",
        "max_length": "密码不能多于18位",
    })
    new_pwd1 = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入旧密码",
        "min_length": "密码不能少于6位",
        "max_length": "密码不能多于18位",
    })
    new_pwd2 = forms.CharField(min_length=8, max_length=18, error_messages={
        "required": "必须输入旧密码",
        "min_length": "密码不能少于6位",
        "max_length": "密码不能多于18位",
    })

    def data_availed(self):
        data_cleaned = self.cleaned_data
        new_password1 = data_cleaned.get("new_pwd1")
        new_password2 = data_cleaned.get("new_pwd2")
        old_password = data_cleaned.get('old_pwd')
        user_id = data_cleaned.get("user_id")
        if not User.objects.filter(pk=user_id).exists():
            self.add_error("user_id", "账户不存在！")
            return False

        user = User.objects.filter(pk=user_id)[0]
        if not user.check_password(old_password):
            self.add_error('old_pwd', '旧密码不正确！')
            return False
        if new_password1 != new_password2:
            self.add_error("new_pwd1", "两次密码输入不一样！")
            return False
        return True
