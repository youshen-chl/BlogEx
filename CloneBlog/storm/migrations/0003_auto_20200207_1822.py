# Generated by Django 2.2.3 on 2020-02-07 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storm', '0002_activate'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='网站名字')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='网站描述')),
                ('link', models.URLField(help_text='请填写http或https开头的完整形式地址', verbose_name='友链地址')),
                ('logo', models.URLField(blank=True, help_text='请填写http或https开头的完整形式地址', verbose_name='友站LOGO')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否首页展示')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'ordering': ['create_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': '文章分类', 'verbose_name_plural': '文章分类'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['id'], 'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
    ]
