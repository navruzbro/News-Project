from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from .models import News, Category, Photography
from .forms import ContactForm


# Create your views here.

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['news'] = News.published.all().order_by("-publish_time")[:5]
        context['local_news'] = News.published.all().filter(category__name="mahalliy")[:10]
        context['xorijiy'] = News.published.all().filter(category__name="xorij")[:10]
        context['texnologiya'] = News.published.all().filter(category__name="texnologiya")[:10]
        context['sport'] = News.published.all().filter(category__name="sport")[:10]
        context['photos'] = Photography.objects.all()[:6]
        return context

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self,request, *args, **kwargs):
        form = ContactForm
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('<h2 style="font-family:sans-serif; background-color:#797979;border-raduis:10px;border:2px solid black; text-align:center; padding:10px; text-decoration:none;color:black;">Biz bilan bog\'langaningiz uchun tashakkur, Tez orada javob beramiz <h2>')
        

def Page404View(request):
    context = {

    }
    return render(request, 'news/404.html', context)


def News_list(request):
    #News_list  = News.objects.filter(status = News.status.Published)
    News_list = News.published.all()
    context = {
        "News_list" : News_list  
            }
    return render(request, "news/news_list.html", context)

def News_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news':news
    }
    return render(request, 'news/news_detail.html', context)


#Category view------

class LocalNewsView(ListView):
    model = News
    template_name = 'news/local.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__name = "mahalliy").order_by("-publish_time")[:5]
        return news
    
class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign.html'
    context_object_name = 'xorijiy_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__name = "xorij").order_by("-publish_time")[:5]
        return news
    

class TechnoNewsView(ListView):
    model = News
    template_name = 'news/techno.html'
    context_object_name = 'texno_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__name = "texnologiya").order_by("-publish_time")[:5]
        return news
    
class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = News.published.all().filter(category__name = "sport").order_by("-publish_time")[:5]
        return news

