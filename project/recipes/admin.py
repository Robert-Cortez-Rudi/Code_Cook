from django.contrib import admin
from .models import Recipe, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...

