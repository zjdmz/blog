"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myblog import settings
from django.conf.urls.static import static
from . import views

# 设置命名空间
app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('learn', views.learn, name='learn'),
    path('share', views.share, name='share'),
    path('energy', views.positive_energy, name='energy'),
    path('about', views.about_me, name='about'),
    path('write_article', views.WriteArticle.as_view(), name='write_article'),
    path('edit_article/<article_id>', views.EditArticle.as_view(), name='edit_article'),
    path('upload/image', views.upload_image, name='upload_image'),
    path('edit_category', views.CategoryMenage.as_view(), name='edit_category'),
    path('del_category', views.del_category, name='del_category'),
    path('article_list', views.article_list, name='article_list'),
    path('del_article', views.del_article, name='del_article'),
]

urlpatterns += static('/media', document_root=settings.MEDIA_ROOT)
