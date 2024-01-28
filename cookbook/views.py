from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.db.models import F, Sum, Case, When, IntegerField

from cookbook.models import Product, Recipe, ProductToRecipe


@api_view(['GET'])
def add_product_to_recipe(request, product_id, recipe_id, weight):
    """Добавление продукта к рецепту (замена граммовки)"""
    try:
        weight = int(weight)
    except ValueError:
        return Response({"status": "error", "message": "Invalid weight format"})
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    with transaction.atomic():
        product_to_recipe, created = ProductToRecipe.objects.get_or_create(
            product=product, recipe=recipe, defaults={'weight': weight}
        )

        if not created:
            product_to_recipe.weight = weight
            product_to_recipe.save()

    return Response({'message': f'{product.name} в кол-ве {weight} г добавлен(а) в рецепт {recipe.name}'})


@api_view(['GET'])
@transaction.atomic
def cook_recipe(request, recipe_id):
    """Приготовление по рецепту (изменение счетчика использования продукта)"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    try:
        with transaction.atomic():
            for product in recipe.ingridients.all():
                product.cook_counter = F('cook_counter') + 1
                product.save(update_fields=['cook_counter'])
    except Exception as e:
        return {'message': 'Возникла ошибка'}
    
    return Response({"message": f"Рецепт приготовлен: {recipe.name}"})


@api_view(['GET'])
def show_recipes_without_product(request, product_id):
    """Таблица рецептов без продукта (использование менее 10 грамм)"""
    product = get_object_or_404(Product, pk=product_id)

    recipe_without_product = (
        Recipe.objects.annotate(
            product_weight=Sum(
                Case(
                    When(producttorecipe__product=product, then='producttorecipe__weight'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
    ).exclude(product_weight__gte=10).distinct()

    return render(request, "cookbook/recipes_without_product.html", {"recipes": recipe_without_product})