from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['uid','title','slug','text','author','status','publish','created','updated']
    list_filter=['title']
    search_fields=['title','text']
    prepopulated_fields={'slug':('title',)}
    show_facets=admin.ShowFacets.ALWAYS
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['uid','user','post','body','created','updated']
    list_filter=['created','updated']
    search_fields=['body']
    show_facets=admin.ShowFacets.ALWAYS