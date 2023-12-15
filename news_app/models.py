from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User 
# Create your models here.


#category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
#News model
class News(models.Model):

    class Status(models.TextChoices):
        Draft = "DF", 'Draft'
        Published = "PB", "Published"
 

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    body = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='media/news/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, 
                              choices=Status.choices,
                              default=Status.Draft
                              )
    
    class Meta:
        ordering = ["-publish_time"]
    
    class PublishedManager(models.Manager):
        def get_queryset(self):
             return super().get_queryset().filter(status = News.Status.Published)
    

    objects = models.Manager()
    published =  PublishedManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("news_detail_page", args=[self.slug])
    

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=180)
    message = models.TextField(max_length=5000)

    def __str__(self):
        return self.email
    
class Photography(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='media/photography/images')
    

    objects = models.Manager()
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='comments')
    body = models.TextField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']
        
    def __str__(self):
        return f'comment {self.body} by {self.user}'