from django.contrib import admin
from .models import News, Category, Contact, Photography 


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