from django.db import models
from django.contrib.auth.models import User # Model de usuário próprio do Django


class Category(models.Model):
    name = models.CharField(max_length=65)


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # No momento da criação ele pega a data
    updated_at = models.DateTimeField(auto_now=True) # Atualiza o valor automaticamente quando for salvo
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to="recipes/covers/%Y/%m/%d") # Só é possivel utilizar se tiver o Pillow instalado
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True # Permite que seja null o campo
    ) # O ForeignKey define uma chave estrangeira
    # on_delete=models.SET_NULL -> Se a categoria for excluída, o campo será definido como NULL, em vez de excluir o objeto relacionado

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True # Permite que seja null o campo
    )

