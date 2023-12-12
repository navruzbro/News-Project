from django.urls import path
from .views import(
    News_list, 
    News_detail, 
    HomePageView, 
    ContactPageView,
    Page404View,
    #category
    LocalNewsView,
    SportNewsView,
    TechnoNewsView,
    ForeignNewsView,
    )

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('news/', News_list, name="all_news_list"),
    path('name/<slug:news>/', News_detail, name="news_detail_page"),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('page-404/', Page404View, name="404_page"),
    #category
    path('mahalliy/', LocalNewsView.as_view(), name="local_news"),
    path('xorijiy/', ForeignNewsView.as_view(), name="foreign_news"),
    path('sport/', SportNewsView.as_view(), name="sport_news"),
    path('texno/', TechnoNewsView.as_view(), name="techno_news"),
]