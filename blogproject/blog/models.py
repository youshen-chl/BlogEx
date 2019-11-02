from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

import markdown
from django.utils.html import strip_tags

class Category(models.Model):
    '''
        分类
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''
        标签
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    '''
        文章
    '''
    title = models.CharField(max_length=70,verbose_name='标题')

    body = models.TextField(verbose_name='正文')

    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now )
    modified_time = models.DateTimeField(verbose_name='修改时间')

    excerpt = models.CharField(verbose_name='摘要',max_length=200, blank=True)

    category = models.ForeignKey(Category,verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,verbose_name='标签', blank=True)

    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    
    # views = models.
    class Meta:
        verbose_name = '已发表的文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        if not self.excerpt:
            self.excerpt = strip_tags(md.convert(self.body))[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk' : self.pk})



