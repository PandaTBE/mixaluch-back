from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("api/news/", views.NewsListView.as_view(), name="news"),
    path(
        "api/important-news/", views.ImportantListView.as_view(), name="important_news"
    ),
]
