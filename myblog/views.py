from django.shortcuts import render, reverse


# Create your views here.

# 博客首页
def index(request):
    return render(request, 'index.html')


# 学无止境页面
def learn(request):
    return render(request, "learn.html")


# 收藏分享页面
def share(request):
    return render(request, "share.html")


# 正能量页面
def positive_energy(request):
    return render(request, "positive-energy.html")


# 关于我
def about_me(request):
    return render(request, "about.html")
