from typing import List

from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=60, unique=True)
    is_spicy = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'toppings'


class Pizza(models.Model):
    name = models.CharField(max_length=60, unique=True)
    is_vegetarian = models.BooleanField()
    toppings = models.ManyToManyField(Topping, related_name='+')

    def __str__(self):
        toppings = ', '.join(str(topping) for topping in self.toppings.all())
        return '%s: is_vegetarian: %s, toppings: %s' % (self.name, self.is_vegetarian, toppings)

    def spicy_toppings_db_filtering(self) -> List[Topping]:
        """
        This function filters out spicy toppings in database.  This is an example of function that should NEVER be
        written since this function can never be optimized.  This would come up in the recommendation as code change
        """
        return list(self.toppings.filter(is_spicy=True))

    def spicy_toppings_python_filtering(self) -> List[Topping]:
        """
        This function filters out spicy toppings in python.  This is an example of a function that can be optimized
        because it allows the programmer to do prefetch_related.  If we miss to do prefetch related, the code
        recommendation would show it as apply prefetch related
        """
        return [topping for topping in self.toppings.all() if topping.is_spicy]

    def toppings_of_best_pizza_serving_restaurants(self) -> List[Topping]:
        """
        This function returns all toppings used in the best pizza of all restaurants serving this pizza
        """
        all_best_pizza = [restaurant.best_pizza for restaurant in self.restaurants.all()]
        return [pizza.toppings.all() for pizza in all_best_pizza]

    class Meta:
        db_table = 'pizza'


class Restaurant(models.Model):
    name = models.CharField(max_length=60, unique=True)
    pizzas = models.ManyToManyField(Pizza, related_name='restaurants')
    best_pizza = models.ForeignKey(Pizza, null=True, related_name='championed_by', on_delete=models.SET_NULL)
    is_active = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'restaurant'
