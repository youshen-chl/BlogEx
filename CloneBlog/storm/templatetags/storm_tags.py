from django import template
from ..models import BigCategory, Category, Activate, Carousel, Article, Tag, FriendLink
from django.utils.html import mark_safe
from django.db.models import Count

register = template.Library()

# 测试用着玩
@register.inclusion_tag('storm/inclusions/_list.html', takes_context=True)
def show_lists(context, num=5):
    numlist = list(range(1,num+1))
    print(numlist)
    return {
        'showlists' : numlist,
    }

# @register.simple_tag
# def print_num(num):
#     return 'this is %d' % num

#显示导航栏组件
@register.inclusion_tag('storm/inclusions/_nav.html', takes_context=True)
def show_nav(context):
    return {
        'bigcategory' : BigCategory.objects.all(),
    }

# 返回文章分类查询集
@register.simple_tag
def get_category_list(id):
    """返回小分类列表"""
    return Category.objects.filter(bigcategory =id)

# 返回公告查询集
@register.simple_tag
def get_active():
    ''' 获得活跃的友情链接 '''
    text = Activate.objects.filter(is_active = True)
    if text:
        text = text[0].text
    else:
        text = ''
    
    return mark_safe(text)

# 显示 右侧 小轮播图
@register.inclusion_tag('storm/inclusions/_carousel_right.html', takes_context=True)
def show_carousel_right(context):
    return {
        'carousels' : Carousel.objects.filter(number__gt=5, number__lte=10)
    }

# 显示 主 轮播图
@register.inclusion_tag('storm/inclusions/_carousel_images.html', takes_context=True)
def show_carousel_images(context):
    return {
        'carousels' : Carousel.objects.filter(number__lte=5)
    }

#显示标签云
@register.inclusion_tag('storm/inclusions/_tag_list.html', takes_context=True)
def show_tag_lists(context):

    return {
        "tag_lists" : Tag.objects.annotate(total_num=Count('article')).filter(total_num__gt=0),
    }

#根据条件筛选提取文章列表
@register.simple_tag
def get_article_list(sort=None, num=5):
    if sort:
        articles = Article.objects.order_by(sort)[:num]
    else:
        articles = Article.objects.all()[:num]
    
    # for c in articles:
    #     print(c.views)

    return articles

#显示文章列表
@register.inclusion_tag('storm/inclusions/_article_list.html', takes_context=True)
def show_article_list(context, articles):

    return {
        'articles' : articles ,
    }

#显示日期分类栏
@register.inclusion_tag('storm/inclusions/_category_date.html', takes_context=True)
def show_category_date(context):

    return {
        'article_dates' : Article.objects.datetimes('create_date', 'month', order='DESC'),
    }

#显示友情链接列表
@register.inclusion_tag('storm/inclusions/_friend_link.html', takes_context=True)
def show_friendlink(context):
    return {
        'friendlinks' : FriendLink.objects.filter(is_active=True, is_show=True) ,
    }