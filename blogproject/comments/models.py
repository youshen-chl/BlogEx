from django.db import models

# Create your models here.
from django.utils import timezone

class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='名字')
    email = models.EmailField(verbose_name='邮箱')
    url = models.URLField(blank=True, verbose_name='网址')
    text = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name='评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])