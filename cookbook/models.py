from django.db import models


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=120, verbose_name="Название")
    cook_counter = models.IntegerField(default=0, verbose_name="Счетчик использования")

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""
    name = models.CharField(max_length=120, verbose_name="Название")
    ingridients = models.ManyToManyField(Product, through='ProductToRecipe', verbose_name="Ингридиенты")

    def __str__(self) -> str:
        return self.name


class ProductToRecipe(models.Model):
    """Промежуточная модель для связи many-to-many"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    weight = models.IntegerField(verbose_name="Вес в граммах")

    def __str__(self):
        return f"{self.recipe.name} - {self.product.name}"
    
    class Meta:
        unique_together = ('recipe', 'product')
