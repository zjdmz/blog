from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import ImgUpload, ArticleCategory, Article, Comment
from cms.models import User
from .forms import CategoryForms, ArticleForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from utils.decorators import blog_login_required
import os, sys, datetime


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


#  图片上传
@require_POST
@login_required(login_url="/login")
def upload_image(request):
    image = request.FILES.get('img')
    filename = image.name
    _, ext = os.path.splitext(filename)
    if ext[1:] in ['png', 'jpeg', 'jpg', 'gif']:
        code = request.POST.get('code')
        article_img = ImgUpload.objects.create(img=image, filename=filename)
        if code == 'article_img':
            return HttpResponse(
                "<script>top.$('.mce-btn.mce-open').parent().find('.mce-textbox').val('/media/%s').closest('.mce-window').find('.mce-primary').click();</script>" % article_img.img)
        return JsonResponse({"thumb_img": '/media/' + str(article_img.img), 'status': 200})
    return JsonResponse({'type_error': '请上传图片类型的文件'})


# 分类管理
@method_decorator(login_required(login_url="/login"), name='dispatch')
class CategoryMenage(View):
    def get(self, request):
        user = User.objects.filter(telephone=request.user)[0]
        if user:
            return render(request, "blog/edit_category.html", context={
                'categorys': user.article_ctg.all()
            })

    def post(self, request):
        forms = CategoryForms(request.POST)
        if forms.is_valid() and forms.availed_user(request):
            category = forms.cleaned_data.get('category')
            code = request.POST.get('code')
            ctg_id = request.POST.get('ctg_id')
            user = User.objects.filter(telephone=request.user)[0]
            if code == 'add':
                ctg = ArticleCategory(category=category, author=user)
                ctg.save()
            else:
                if ArticleCategory.objects.filter(pk=ctg_id).exists():
                    ctg = ArticleCategory.objects.filter(pk=ctg_id)[0]
                    ctg.category = category
                    ctg.save()
                else:
                    return JsonResponse({'message': '分类不存在'})

            return JsonResponse({'message': ctg.category})
        form_error = forms.errors.get_json_data().popitem()[1][0]["message"]
        return JsonResponse({'message': form_error})


#  删除分类
@login_required(login_url="/login")
def del_category(request):
    ctg_id = request.GET.get('ctg_id')
    print(ctg_id)
    if ArticleCategory.objects.filter(pk=ctg_id).exists():
        ArticleCategory.objects.get(pk=ctg_id).delete()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'message': 'error'})


# 新增文章
@method_decorator(login_required(login_url="/login"), name='dispatch')
class WriteArticle(View):
    def get(self, request):
        user = User.objects.filter(telephone=request.user)[0]
        if user:
            content = {
                'categorys': user.article_ctg.all()
            }
        else:
            content = {'categorys': None}
        return render(request, "blog/write_article.html", context=content)

    def post(self, request):
        title = request.POST.get('title')

        thumb_url = request.POST.get('thumb_url')
        category_id = request.POST.get('category')
        content = request.POST.get('content')
        forms = ArticleForm(request.POST)
        if forms.is_valid():
            article = Article.objects.create(title=title, thumbnail=thumb_url,
                                             category=ArticleCategory.objects.get(pk=category_id), content=content,
                                             last_update=datetime.datetime.now(), author=request.user,
                                             is_active=True)
            return redirect(reverse('blog:article_list'))
        form_error = forms.errors.get_json_data().popitem()[1][0]["message"]

        return JsonResponse({'message': form_error})


# 文章列表
@login_required(login_url="/login")
def article_list(request):
    articles = Article.objects.filter(author=request.user).all()
    return render(request, 'blog/list_article.html', context={'articles': articles})


# 编辑文章
@method_decorator(login_required(login_url="/login"), name='dispatch')
class EditArticle(View):
    def get(self, request, article_id):
        if Article.objects.filter(pk=article_id, author=request.user).exists():
            context = {'article': Article.objects.get(pk=article_id),
                       'categorys': ArticleCategory.objects.filter(author=request.user).all()
                       }
        else:
            context = {'article': None}
        return render(request, 'blog/write_article.html', context=context)

    def post(self, request, article_id):
        print('article_id = ', article_id)
        if Article.objects.filter(pk=article_id, author=request.user).exists():
            title = request.POST.get('title')
            thumb_url = request.POST.get('thumb_url')
            category_id = request.POST.get('category')
            content = request.POST.get('content')
            forms = ArticleForm(request.POST)
            if forms.is_valid():
                Article.objects.filter(pk=article_id).update(title=title, thumbnail=thumb_url, category_id=category_id,
                                                             content=content, last_update=datetime.datetime.now())
            return redirect(reverse("blog:article_list"))


# 删除文章
@login_required(login_url="/login")
@require_GET
def del_article(request):
    article_id = request.GET.get('article_id')
    if Article.objects.filter(pk=article_id, author=request.user).exists():
        Article.objects.filter(pk=article_id).delete()
        return JsonResponse({"message": 'OK'})
    else:
        return JsonResponse({"message": 'error'})
