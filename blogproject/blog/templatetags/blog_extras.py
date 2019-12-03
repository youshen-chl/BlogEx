from django import template

from blog.models import Category, Post, Tag

register = template.Library()

@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list' : Post.objects.all()[:num],
    }

@register.simple_tag
def show_archives_num(year, month):
    return Post.objects.filter(created_time__year=year, created_time__month=month).count()
# def show_archives_num():
#     return 2

@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list' : Post.objects.dates('created_time', 'month', order='DESC'),
        # 'show_archives_num' : show_archives_num,
    }

@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list' : Category.objects.all(),
    }

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list' : Tag.objects.all(),
    }
