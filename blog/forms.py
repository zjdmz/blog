# -*-coding:utf-8 -*-


from django import forms
from cms.models import User

# 分类
class CategoryForms(forms.Form):
    category = forms.CharField(max_length=20,min_length=1,error_messages={
        'required':'请输入分类名字',
        'max_length':'分类名字不能过长',
        'min_length' : '分类名字太短了'
    })

    def availed_user(self,request):
        user = User.objects.filter(telephone=request.user)[0]
        if user:
            return True
        else:
            return False


# 文章
class ArticleForm(forms.Form):
    title = forms.CharField(max_length=100)
    category = forms.IntegerField()
    # thumb_url = forms.URLField(required=False)
    content = forms.CharField(required=True,min_length=10,error_messages={
        'required': '请编辑文章内容',
        'min_length': '文字内容不能少于10个字'
    })

