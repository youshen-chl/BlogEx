from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title','body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        #from django.utils import timezone
        #obj.created_time = timezone.now()
        #obj.modified_time = timezone.now()
        super().save_model(request,obj, form, change)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)