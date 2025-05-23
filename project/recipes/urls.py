from django.urls import path
from . import views

app_name = "codecook"

urlpatterns = [
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path("recipes/category/<int:category_id>/", views.category, name="category"),
    path("recipes/<int:id>/", views.recipe, name="recipe"),
    path("recipes/search/", views.search, name="search")
]
