from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('django_query_profiler/', include('django_query_profiler.client.urls'))
]
