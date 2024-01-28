from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название")
    cook_counter = models.IntegerField(default=0, verbose_name="Счетчик использования")

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название")
    ingridients = models.ManyToManyField(Product, through='ProductToRecipe', verbose_name="Ингридиенты")

    def __str__(self) -> str:
        return self.name


class ProductToRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.recipe.name} - {self.product.name}"
    
    class Meta:
        unique_together = ('recipe', 'product')
