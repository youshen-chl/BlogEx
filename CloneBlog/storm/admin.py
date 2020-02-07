from django.contrib import admin

# Register your models here.
from .models import Article, BigCategory, Category, Carousel, Tag, Keyword, FriendLink

# 自定义管理站点的名称和URL标题
admin.site.site_header = '网站管理'
admin.site.site_title = '博客后台管理'


@admin.register(BigCategory)
class BigCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'title', 'content', 'img_url','url')
    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'create_date'
    filter_horizontal = ('tags', 'keywords')
    list_display = ('id', 'title', 'author', 'create_date', 'update_date')

    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)

    list_per_page = 50  # 控制每页显示的对象数量，默认是100


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ('name','description','link','create_date','is_active','is_show')
    date_hierarchy = 'create_date'
    list_filter = ('is_active', 'is_show')