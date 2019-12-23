from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from .models import Pizza, Restaurant


def index(request: WSGIRequest) -> HttpResponse:
    # No prefetches anywhere
    pizzas = Pizza.objects.all()

    [pizza.spicy_toppings_db_filtering() for pizza in pizzas]
    [pizza.spicy_toppings_python_filtering() for pizza in pizzas]
    [pizza.toppings_of_best_pizza_serving_restaurants() for pizza in pizzas]

    # # No prefetches anywhere
    [pizza.spicy_toppings_db_filtering() for pizza in Pizza.objects.prefetch_related('toppings').all()]
    [pizza.spicy_toppings_python_filtering() for pizza in Pizza.objects.prefetch_related('toppings').all()]
    [pizza.toppings_of_best_pizza_serving_restaurants() for pizza in Pizza.objects.prefetch_related('toppings').all()]
    list(Restaurant.objects.all())

    return HttpResponse("Made all the db calls, now test the calls made via profiler")
