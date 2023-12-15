from django.contrib import admin
from .models import News, Category, Contact, Photography, Comment


# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title","slug","publish_time","status"]
    list_filter = ["status","created_time"]
    prepopulated_fields = {"slug":("title",)}
    date_hierarchy = "publish_time"
    search_fields = ['title','body']
    ordering = ['status','publish_time']

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Contact)

admin.site.register(Photography)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','news','body','created_time','active']
    list_filter = ['active','created_time','news',]
    search_fields = ['user','body']
    actions = ['disable_comments','activate_comments']
    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Comment, CommentAdmin)