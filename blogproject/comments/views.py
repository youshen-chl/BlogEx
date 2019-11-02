from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST

from .form import CommentForm
from  django.contrib import messages
# Create your views here.

@require_POST
def comment(request, post_pk):
    ''' comment view handler '''
    post = get_object_or_404(Post, pk=post_pk)

    form = CommentForm(request.POST)

    # 当调用 form.is_valid() 方法时，django 自动帮我们检查表单的数据是否符合格式要求。
    if form.is_valid() :
        commit = form.save(commit=False)

        commit.post = post

        commit.save()
        messages.add_message(request,messages.SUCCESS,'评论发表成功！', extra_tags='success')
        return redirect(post)

    context = {
        'post' : post,
        'form' : form,
    }
    messages.add_message(request,messages.ERROR,'评论发表失败，请修改错误后重新提交！', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)