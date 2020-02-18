from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticleComment, CommentUser, AboutselfComment, MessageComment
from storm.models import Article
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import re
# Create your views here.

# 确定重复是否重复
def confirm(new_content, comment_post_ID, auser):
    if comment_post_ID == 'about':
        res = AboutselfComment.objects.filter(content=new_content, author=auser)
    elif comment_post_ID == 'message':
        res = MessageComment.objects.filter(content=new_content, author=auser)
    else:
        res = ArticleComment.objects.filter(content=new_content, author=auser, belong_id=comment_post_ID)
    if res:
        return False
    else:
        return True


# @login_required
@csrf_exempt
@require_POST
def AddcommentView(request):

    if request.is_ajax():
        data = request.POST
        #评论内容
        new_content = data.get('w')
        #评论对象， 指的是 页面留言/文章等等
        comment_post_ID = data.get('comment_post_ID')
        # 父级 

        # 评论者
        author = data.get('author', '')
        # 评论者邮箱
        email = data.get('email', '')
        #评论者网址
        url = data.get('url', '')

        #验证信息格式
        if not re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
            return HttpResponse('请输入有效的邮箱格式！', content_type='text/html;charset="utf-8"', status=405)
        if not new_content:
            return HttpResponse('请写点内容...', content_type='text/html;charset="utf-8"', status=405)
        if not author or not email:
            return HttpResponse('请填入邮箱和昵称',content_type='text/html;charset="utf-8"', status=405)

        # 存储评论者信息
        auser, _ = CommentUser.objects.get_or_create(nickname=author, email=email, address=url)
        # 父级对象
        comment_parent = data.get('comment_parent')

        if not confirm(new_content, comment_post_ID, auser):
            return HttpResponse('请勿发表重复内容！', content_type='text/html;charset="utf-8"', status=405)

        """
        存储评论信息
        """

        # 关于自己页面评论
        if comment_post_ID == 'about':
            # 父级评论
            if comment_parent == '0':
                new_comment = AboutselfComment(author=auser, content=new_content, parent=None, rep_to=None)
            # 评论他人评论
            else:
                parent = AboutselfComment.objects.get(id=comment_parent)
                new_comment = AboutselfComment(author=auser, content=new_content, parent=parent, rep_to=None)
            new_comment.save()
        # 给我留言页面评论
        elif comment_post_ID == 'message':
            if comment_parent == '0':
                new_comment = MessageComment(MessageComment, auser, new_content)
            else:
                parent = MessageComment.objects.get(id=comment_parent)
                new_comment = MessageComment(author=auser, content=new_content, parent=parent, rep_to=None)
            new_comment.save()
        # 文章评论
        else:
            the_article = Article.objects.get(id=comment_post_ID)
            if comment_parent == '0':
                new_comment = ArticleComment(author=auser, content=new_content, belong=the_article, parent=None, rep_to=None)
            else:
                parent = ArticleComment.objects.get(id=comment_parent)
                new_comment = ArticleComment(author=auser, content=new_content, belong=the_article, parent=parent, rep_to=None)
            new_comment.save()

        # 获取用什么身份，分登陆身份和游民身份
        request.session['nick'] = new_comment.author.nickname
        request.session['tid'] = new_comment.author.id
# 返回当前评论，直接返回HTML内容刚给前端，使用JS在指定位置进行数据展示
        return HttpResponse('''<li class="" id="comment-">
                <div class="c-avatar"><img alt='' src='https://cuiqingcai.com/avatar/.png' class='avatar avatar-54 photo avatar-default' height='54' width='54' />
                <div class="c-main" id="div-comment-">{0}
                <div class="c-meta"><span class="c-author">{1}</span>
                </div>
                </div>
                </div>'''.format(new_content, author), content_type='text/html;charset="utf-8"')

    return HttpResponse('参数错误', content_type='text/html;charset="utf-8"')