from tests.testapp.food.models import Pizza, Restaurant, Topping


def bulk_create_toppings_pizzas_restaurants() -> None:
    olives = Topping.objects.create(name='olives', is_spicy=False)
    pineapple = Topping.objects.create(name='pineapple', is_spicy=False)
    pepperoni = Topping.objects.create(name='pepperoni', is_spicy=True)
    canadian_bacon = Topping.objects.create(name='canadian_bacon', is_spicy=True)
    mozzarella = Topping.objects.create(name='mozzarella', is_spicy=False)

    pepperoni_pizza = Pizza.objects.create(name='Pepperoni', is_vegetarian=False)
    pepperoni_pizza.toppings.add(pepperoni)
    pepperoni_pizza.toppings.add(olives)

    bacon_pizza = Pizza.objects.create(name='bacon', is_vegetarian=False)
    bacon_pizza.toppings.add(canadian_bacon)
    bacon_pizza.toppings.add(mozzarella)

    pineapple_pizza = Pizza.objects.create(name='pineapple', is_vegetarian=True)
    pineapple_pizza.toppings.add(pineapple)
    pineapple_pizza.toppings.add(mozzarella)
    pineapple_pizza.toppings.add(olives)

    # Creating some restaurant
    north_beach_restaurant = Restaurant.objects.create(
        name='North Beach',
        best_pizza=pepperoni_pizza,
        is_active=True)
    north_beach_restaurant.pizzas.add(pepperoni_pizza)
    north_beach_restaurant.pizzas.add(pineapple_pizza)

    amici_restaurant = Restaurant.objects.create(
        name='Amici',
        best_pizza=pineapple_pizza,
        is_active=True)
    amici_restaurant.pizzas.add(pepperoni_pizza)
    amici_restaurant.pizzas.add(pineapple_pizza)
    amici_restaurant.pizzas.add(bacon_pizza)


def bulk_create_toppings() -> None:
    olives = Topping(name='olives', is_spicy=False)
    pineapple = Topping(name='pineapple', is_spicy=False)
    pepperoni = Topping(name='pepperoni', is_spicy=True)
    canadian_bacon = Topping(name='canadian_bacon', is_spicy=True)
    mozzarella = Topping(name='mozzarella', is_spicy=False)

    Topping.objects.bulk_create([olives, pineapple, pepperoni, canadian_bacon, mozzarella])
