from django.contrib import admin

from cookbook.models import Product, Recipe


admin.site.register(Product)


class RecipeInLine(admin.TabularInline):
    model = Recipe.ingridients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка admin-панели для рецептов"""
    inlines = (RecipeInLine,)
    exclude = ('ingridients',)
