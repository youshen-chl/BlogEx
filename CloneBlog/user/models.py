from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Ouser(AbstractUser):
    #继承至AbsotractUser （Django自带用户基类）

    # 拓展用户个人网站地址字段
    link = models.URLField('个人网站', blank=True, help_text='提示：网址必须填写以http开头的完整形式')

    # 拓展用户头像字段
    avatar = ProcessedImageField(
        upload_to = 'avatar/%Y/%m/%d',
        default='avatar/default.png',
        verbose_name='头像',
        processor=[ResizeToFill(80,80)]
    )

    class Meta:
        verbose_name='用户'
        verbose_name_plural=verbose_name
        ordering=['-id']

    def __str__(self):
        return self.username
        