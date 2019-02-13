# _*_ coding:utf-8 _*_

from django.db import models


class ArticleCategory(models.Model):
    # 文章分类
    category = models.CharField(max_length=100)
    author = models.ForeignKey("cms.User", on_delete=models.CASCADE, related_name='article_ctg', default=None)


class Article(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()
    content = models.TextField()
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_update = models.DateTimeField("最近更新时间", auto_now=True)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey("cms.User", on_delete=models.CASCADE, related_name="articles", default=None)
    category = models.ForeignKey("ArticleCategory", on_delete=False, related_name='articles', default=None)

    class Meta:
        ordering = ["-last_update"]

    def create_times(self):
        return self.create_time.strftime("%Y年%m月%d日  %H:%M:%S")

    def last_updates(self):
        return self.last_update.strftime("%Y年%m月%d日  %H:%M:%S")


class Comment(models.Model):
    content = models.TimeField()
    create_time = models.TimeField('创建时间', auto_now_add=True)
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("cms.User", on_delete=models.CASCADE, related_name="comments", default=None)

    class Meta:
        ordering = ["-create_time"]


class ImgUpload(models.Model):
    filename = models.CharField(max_length=200, blank=True, null=True)
    img = models.ImageField(upload_to='article_img')
