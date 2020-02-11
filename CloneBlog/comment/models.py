from django.db import models

# Create your models here.
from django.conf import settings
from storm.models import Article

import markdown
import emoji

class CommentUser(models.Model):
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    email = models.CharField(max_length=30, verbose_name='邮箱')
    address = models.CharField(max_length=200, verbose_name='地址')


class Comment(models.Model):
    author = models.ForeignKey(CommentUser, related_name='%(class)%_related', verbose_name='评论人')
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    content = models.TextField('评论内容')
    parent = models.ForeignKey('self', verbose_name='父评论', related_name='%(class)%_child_comments', blank=True, null=True)
    rep_to = models.ForeignKey('self', verbose_name='回复', related_name='%(class)%_rep_comments', blank=True, null=True)

    class Meta:
        abstract = True


    def __str__(self):
        return self.content[:20]

    def content_to_markdown(self):
        # 先转换成emoji然后转换成markdown,'escape':所有原始HTML将被转义并包含在文档中
        to_emoji_content = emoji.emojize(self.content, use_aliases=True)
        to_md = markdown.markdown(to_emoji_content,
                                safe_mode='escape',
                                extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite'
                                ]
                            )
        return to_md



    