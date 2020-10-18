from django.urls import path

from .views import CategoryView, IllustView

app_name = 'illust_list'

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category'),
    path('illust_list/', IllustView.as_view(), name='illust_list'),
]