from django.contrib import admin
from .models import Post,Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['author', 'title','image','content','created_date']

class CommentAdmin(admin.ModelAdmin):
    list_display=['commentor','post','content']