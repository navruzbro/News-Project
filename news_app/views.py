from typing import Any
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, CreateView
from .models import News, Category, Photography, Comment
from .forms import ContactForm, CommentForm
from django.utils.text import slugify
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin
from config.custom_permissions import OnlySuperUser
from django.contrib.auth.decorators import user_passes_test, login_required

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

    def get(self, request, *args, **kwargs):
        form = ContactForm
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse(
                '<h2 style="font-family:sans-serif; background-color:#797979;border-raduis:10px;border:2px solid black; text-align:center; padding:10px; text-decoration:none;color:black;">Biz bilan bog\'langaningiz uchun tashakkur, Tez orada javob beramiz <h2>')


def Page404View(request):
    context = {

    }
    return render(request, 'news/404.html', context)


def News_list(request):
    # News_list  = News.objects.filter(status = News.status.Published)
    News_list = News.published.all()
    context = {
        "News_list": News_list
    }
    return render(request, "news/news_list.html", context)


def News_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    #hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk':hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    
    comments = news.comments.filter(active=True)[:10]
    comments_all = news.comments.filter(active=True)
    comments_count = comments_all.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'comments_all':comments_all,
        'new_comment': new_comment,
        'comments_count':comments_count,
        'comment_form': comment_form,
    }
    return render(request, 'news/news_detail.html', context)


# Category view------

class LocalNewsView(ListView):
    model = News
    template_name = 'category/local.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__name="mahalliy").order_by("-publish_time")[:15]
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'category/foreign.html'
    context_object_name = 'xorijiy_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__name="xorij").order_by("-publish_time")[:15]
        return news


class TechnoNewsView(ListView):
    model = News
    template_name = 'category/techno.html'
    context_object_name = 'texno_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__name="texnologiya").order_by("-publish_time")[:15]
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'category/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = News.published.all().filter(category__name="sport").order_by("-publish_time")[:15]
        return news


# Update Create Delete VIEWS

class NewsCreateView(OnlySuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'image', 'category', 'image', 'category', 'status')


class NewsUpdateView(OnlySuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlySuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home')


# small admin page

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin.html', context)


class SearchResultsList(ListView):
    models = News
    template_name = 'news/search_results.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        )
