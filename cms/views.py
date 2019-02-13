from django.shortcuts import render, redirect, reverse
from django.core.cache import cache, caches
from django.core.mail import send_mail
from django.views.generic import View
from .forms import LoginForm, RegisterForm, RegisterForm2, UpdateForm, UpdatePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.decorators import blog_login_required
from utils.captcha.hycaptcha import Captcha
from utils.aliyun_sms.sms_send import send_sms
from myblog.settings import DEFAULT_FROM_EMAIL
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import User
import uuid, time, json, threading


# Create your views here.

# 登录
class LoginView(View):
    def get(self, request):

        return render(request, "cms/login-2.html")

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=telephone, password=password)
            if user:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)  # none 默认过期时间，14天
                else:
                    request.session.set_expiry(0)  # 浏览器关闭就过期
                return redirect(reverse("blog:index"))
            else:
                messages.info(request, "用户名/密码错误！")
                return redirect(reverse("cms:login"))
        else:
            form_error = form.errors.get_json_data().popitem()[1][0]["message"]
            messages.info(request, form_error)
            print("login form_error = ", form_error)
            return redirect(reverse("cms:login"))


# 退出登录
def log_out(request):
    logout(request)
    return redirect('/')


# 注册
class RegisterView(View):
    def get(self, request):
        return render(request, "cms/login-2.html")

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid() and form.availed_data(request):
            username = form.cleaned_data.get("username1", None)
            if username == None:
                username = str(uuid.uuid4()).replace("_", "")
            telephone = form.cleaned_data.get("telephone1")
            email = form.cleaned_data.get("email1", None)
            password2 = form.cleaned_data.get("password2")
            remember = form.cleaned_data.get("remember1")
            user = User.objects.create_user(username=username, telephone=telephone, email=email, password=password2)
            login(request, user)
            if remember:
                request.session.set_expiry(None)  # none 默认过期时间，14天
            else:
                request.session.set_expiry(0)  # 浏览器关闭就过期
            result = {'code': 200, "data": "hello world !"}
            return JsonResponse(result)
        else:
            form_error = form.errors.get_json_data().popitem()[1][0]["message"]
            result = {"code": 404, "messages": form_error}
            return JsonResponse(result)


# 注册2
class RegisterView2(View):
    def get(self, request):
        return render(request, "cms/login-2.html")

    def post(self, request):
        form = RegisterForm2(request.POST)
        if form.is_valid() and form.availed_data():
            username = str(uuid.uuid4()).replace("-", "")[:8]
            telephone = form.cleaned_data.get("telephone2")
            password2 = form.cleaned_data.get("password2")
            remember = form.cleaned_data.get("remember2")
            user = User.objects.create_user(username=username, telephone=telephone, password=password2)
            login(request, user)
            if remember:
                request.session.set_expiry(None)  # none 默认过期时间，14天
            else:
                request.session.set_expiry(0)  # 浏览器关闭就过期
            result = {'code': 200, "data": "hello world !"}
            return JsonResponse(result)
        else:
            form_error = form.errors.get_json_data().popitem()[1][0]["message"]
            result = {"code": 404, "messages": form_error}
            return JsonResponse(result)


# 图片验证码
def img_captcha(request):
    text, image = Captcha.gene_code()
    out = BytesIO()  # 这里需要将文件转换成 数据流
    image.save(out, 'png')
    response = HttpResponse(content_type='image/png')

    out.seek(0)
    response.write(out.read())  # out.getvalue() 也可以获取文件数据，但获取文件大小时困难些

    response['Content-length'] = out.tell()  # tell返回当前读写位置，此时指针已经到末尾
    request.session['img_captcha'] = text.lower()  # 将验证码存入session会话
    print("img_captcha_session = ", text.lower())
    return response


# 短信验证码
def send_sms_captcha(request):
    telephone = request.GET.get('telephone')  # 获取从浏览器传来的手机号码
    print(telephone)
    if User.objects.filter(telephone=telephone).exists():
        return JsonResponse({"code": 302, "message": "手机号码已注册"})
    text = cache.get(telephone)
    if not text:
        code = Captcha.gene_text()  # 生成4位短信验证码
        result = send_sms(telephone, code=code)  # 发送验证码并返回发送结果
        result_status = json.loads(result)["Code"]  # 获取短信验证码发送状态
        print(result_status)
        # result_status = "OK"
        # request.session['sms_captcha'] = code  # 设置session 会话中的短信验证码
    else:
        code = text
        result_status = "repeat"
    if result_status == "OK":  # 发送成功
        print("短信验证码为：", code)
        cache.set(telephone, code, 300)
        result = "OK"
    elif result_status == "repeat":  # 验证码 n 秒 内有效
        result = "repeat"
        print("验证码 n 秒 内有效哦！")
    elif result_status == "isv.MOBILE_NUMBER_ILLEGAL":
        result = 'telephone error'
    else:
        print("验证码发送败，错误码：", result_status)
        result = 404
    return JsonResponse({"code": result})


# 编辑个人信息 页面
@login_required(login_url="/login")
def edit_account(request):
    return render(request, 'cms/edit_account.html')


# 编辑个人信息 提交
@login_required(login_url="/login")
def update_account(request):
    print(request.user, 'username')

    if request.method == "POST":
        forms = UpdateForm(request.POST)
        if forms.is_valid() and forms.availed_data():
            username = request.POST.get("username")
            email = request.POST.get("email")
            email_captcha = request.POST.get("email_captcha")
            telephone = request.POST.get("telephone")
            sms_captcha = request.POST.get("sms_captcha")
            user_id = request.POST.get("user_id")
            user = User.objects.filter(pk=user_id)[0]
            s = False
            if user.username != username:
                user.username = username
                s = True
            if user.telephone != telephone and sms_captcha.strip() == cache.get('telephone'):
                user.telephone = telephone
                s = True
            if user.email != email and email_captcha.strip() == cache.get('email'):
                user.email = email
                s = True
            if s:
                user.save()
                return JsonResponse({"code": "200", "message": "修改成功！"})
            else:
                return JsonResponse({"code": "302", "message": "未做修改！"})
        form_error = forms.errors.get_json_data().popitem()[1][0]["message"]
        return JsonResponse({"code": "404", "message": form_error})
    return JsonResponse({"code": "404", "message": "请求错误！"})


# 修改密码
@method_decorator(blog_login_required, name='dispatch')
class UpdatePassword(View):
    def get(self, request):
        print(request.user, 'username')

        return render(request, "cms/edit_password.html")

    def post(self, request):
        forms = UpdatePasswordForm(request.POST)
        if forms.is_valid() and forms.data_availed():
            new_password2 = forms.cleaned_data.get('new_pwd1')
            print(new_password2, '= new_password2')
            user_id = forms.cleaned_data.get('user_id')
            user = User.objects.filter(pk=user_id).first()
            user.set_password(new_password2)
            user.save()
            return JsonResponse({'code': 200, 'message': '密码修改成功'})
        form_error = forms.errors.get_json_data().popitem()[1][0]["message"]
        print(form_error)
        return JsonResponse({'code': 404, 'message': form_error})


# 发送邮件
def send_emails(request):
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，
    code = Captcha.gene_text().lower()  # 生成4位验证码
    email = request.GET.get('email')
    print('email = ', email)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"message": "该邮箱已被绑定"})
    email_title = "【盘根学院邮箱激活码】"
    email_body = "盘根学院邮箱激活码：%s ，激活码5分钟内有效！" % code
    email_cache = cache.get(email)
    print('email_cache = ', email_cache)
    if not email_cache:
        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        cache.set(email, code, 300)
        message = '邮件已发送'
    else:
        message = '验证码5分钟内有效哦！'
    return JsonResponse({'code': code, 'message': message})
