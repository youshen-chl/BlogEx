from django.db import models
from django.conf import settings
# Create your models here.
from django.shortcuts import reverse

import markdown
import re

# 关键词
class Keyword(models.Model):
    name = models.CharField('文章关键词',max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,
                    help_text='用来作为SEO中的description, 长度参考SEO标准')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'tag': self.name})

    def get_article_list(self):
        return Article.objects.filter(tags=self)

# 网站导航菜单栏分类表
class BigCategory(models.Model):
    name = models.CharField('导航栏大分类', max_length=20)

    # 用作文章的访问路径  **/category/**
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240,
        default=settings.SITE_DESCRIPTION,
        help_text='用来作为SEO中的description, 长度参考SEO标准'
    )
    keywords = models.TextField('关键字', max_length=240, 
        default=settings.SITE_KEYWORDS,
        help_text='用来作为SEO中的keywords, 长度参考SEO标准'
    )

    class Meta:
        verbose_name = '导航栏分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 导航栏，分类下的下拉擦菜单分类
class Category(models.Model):
    name = models.CharField('文章分类', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240,
        default=settings.SITE_DESCRIPTION,
        help_text='用来作为SEO中的description, 长度参考SEO标准'
    )
    bigcategory = models.ForeignKey(BigCategory, verbose_name='大分类', on_delete=models.CASCADE())

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category',
                kwargs={'slug': self.slug, 'bigslug': self.bigcategory.slug}
        )

    def get_article_list(self):
        return Article.objects.filter(category=self)

# 文章
class Article(models.Model):
    IMG_LINK = '/static/images/summary.jpg'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.SET_NULL )
    title = models.CharField(max_length=150, verbose_name='文章标题')
    summary = models.TextField(max_length=240, verbose_name='文章摘要', 
                    default='文章摘要等同于网页description内容，请务必填写...'    )
    body = models.TextField(verbose_name='文章内容')
    img_link = models.CharField(verbose_name='图片地址', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField(verbose_name='阅读量', default=0)
    loves = models.IntegerField(verbose_name='喜欢量', default=0)

    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签' )
    keywords = models.ManyToManyField(Keyword, verbose_name='文章关键字',
                help_text='文章关键字，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.update_date = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        if not self.summary:
            self.summary = strip_tags(md.convert(self.body))[:50]
        super().save(*args, **kwargs)

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()

# 幻灯片
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='标题可以为空'    )
    content = models.CharField('描述', max_length=80)
    img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#为不跳转')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前， 添加时间越晚越靠前
        ordering = ['number', '-id']