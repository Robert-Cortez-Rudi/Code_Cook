from django import forms
from project.recipes.models import Recipe
from utils.django_forms import add_attrs
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._errors = defaultdict(list)

        add_attrs(self.fields.get("preparation_steps"), "class", "span-2")

    class Meta:
        model = Recipe
        fields = ["title", "description", "preparation_time", "preparation_time_unit", 
                "servings", "servings_unit", "preparation_steps", "cover"
        ]
        widgets = {
            "cover": forms.FileInput(
                attrs= {
                    "class": "span-2"
                }
            ),
            "servings_unit": forms.Select(
                choices=(
                    ("Porções", "Porções"),
                    ("Pedaços", "Pedaços"),
                    ("Pessoas", "Pessoas")
                )
            ),
            "preparation_time_unit": forms.Select(
                choices=(
                    ("Minutos", "Minutos"),
                    ("Horas", "Horas")
                )
            )
        }


    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")

        if title == description:
            self.errors["title"].append("Cannot to be equal to description")
            self.errors["description"].append("Cannot to be equal to title")

        if self._errors:
            raise ValidationError(self._errors)

        return super_clean


    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 5:
            self._errors["title"].append("Title must have more at least 5 characters!")

        return title


    def clean_preparation_time(self):
        field_name = "preparation_time"
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(self.cleaned_data.get("preparation_time")):
            self._errors[field_name].append("Must be a positiv number!")

        return field_value


    def clean_servings(self):
        field_name = "servings"
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(self.cleaned_data.get("servings")):
            self._errors[field_name].append("Must be a positiv number!")

        return field_value

