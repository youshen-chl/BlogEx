from django import template
from ..models import BigCategory, Category


register = template.Library()

@register.inclusion_tag('storm/inclusions/_list.html', takes_context=True)
def show_lists(context, num=5):
    numlist = list(range(1,num+1))
    print(numlist)
    return {
        'showlists' : numlist,
    }

@register.simple_tag
def print_num(num):
    return 'this is %d' % num

@register.inclusion_tag('storm/inclusions/_nav.html', takes_context=True)
def show_nav(context):
    return {
        'bigcategory' : BigCategory.objects.all(),
    }


@register.simple_tag
def get_category_list(id):
    """返回小分类列表"""
    return Category.objects.filter(bigcategory =id)