from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Article, BigCategory, Category, Tag
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import time, markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

class HomePageView(TemplateView):
    template_name = 'index_main.html'

class IndexView(ListView):
    ''' 首页视图， 用于展示从数据库中获取的文章列表 '''
    #指定数据来源
    model = Article

    # template_name 属性用于指定所使用的 模板

    #指定 返回给模板中使用的 上下文变量名称， 表示文章列表
    context_object_name = 'articles'


    def get_queryset(self):
        ''' get_queryset函数： 返回用于检索该视图将要展示的对象的 数据集合 '''
        
        # 先调用父类的方法，获取 数据集合
        queryset = super(IndexView, self).get_queryset()

        # 提取 url路由 传入的参数
            # 归档日期
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)
            # 标签
        tag = self.kwargs.get('tag', 0)

            # 导航栏
        self.big_slug = self.kwargs.get('big_slug', '')
            # 文章分类
        slug = self.kwargs.get('slug', '')

        # 按类型查询
        if self.big_slug:
            # 如果url中传入了 导航分类big_slug， 筛选出属于该分类的部分文章
            big = get_object_or_404(BigCategory, slug=self.big_slug)
            queryset = queryset.filter(category__bigcategory=big)
            
            if slug:
                # 如果 同时传入了 文章分类slug, 则再筛选出该分类下的文章
                slu = get_object_or_404(Category, slug=slug)
                queryset = queryset.filter(category=slu)

        # 按日期查询
        if year and month:
            queryset = get_list_or_404(queryset, create_date__year=year, create_date__month=month)

        # 按标签查询
        if tag:
            tags = get_object_or_404(Tag, name=tag)
            queryset = queryset.filter(tags=tags)
            self.big_slug = BigCategory.objects.filter(category__article__tags=tags)
            self.big_slug = self.big_slug[0].slug
        
        return queryset

    def get_context_data(self, **kwargs):
        ''' 返回用于显示对象列表的上下文数据 
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。    
        '''
        context = super(IndexView,self).get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。

        paginator = context.get('paginator')
        page = context.get('page')
        is_paginated = context.get('is_paginated')

        #返回的是一个字典
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        context['category'] = self.big_slug

        return context

    def pagination_data(self, paginator, page_obj, is_paginated):
        if not is_paginated:
            # 如果没有分页
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more=True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more=True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class ArticleView(DetailView):
    '''
        Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
    '''
    
    model = Article

    template_name = 'article.html'    

    context_object_name = 'article'

    def get_object(self):
        obj = super(ArticleView, self).get_object()

    # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user
        ses = self.request.session
        # print(u, ses)
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)

        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 *30:
                    obj.update_views()
                    ses[the_key] = now_time
        
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),    
        ])

        obj.body = md.convert(obj.body)
        obj.toc = md.toc
        return obj

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['category'] = self.object.id
        return context


@csrf_exempt
def LoveView(request):
    data_id = request.POST.get('um_id', '')
    if data_id:
        art = Article.objects.get(id=data_id)
        art.loves += 1
        art.save()
        return HttpResponse(art.loves)
    else:
        return HttpResponse('error', status=405)