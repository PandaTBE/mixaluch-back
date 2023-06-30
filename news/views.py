from news.serializers import NewsSerializer
from rest_framework import generics
from news.models import News


# Create your views here.
class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ImportantListView(generics.ListAPIView):
    queryset = News.objects.filter(is_important=True)
    serializer_class = NewsSerializer
