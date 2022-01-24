from django.urls import include, path

from tests.testapp.food import views

urlpatterns = [
    path('', views.index, name='index'),
    path('django_query_profiler/', include('django_query_profiler.client.urls'))
]
