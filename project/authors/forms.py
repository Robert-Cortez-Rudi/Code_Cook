from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attrs(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attr} {attr_new_val}".strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs["placeholder"] = f"{placeholder_val}".strip()


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError(
            """Password must have at least one uppercase letter, one lowercase letter and one number.
            The length should be at least 8 characters.""", code="invalid")
    

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"],"Your username")
        add_placeholder(self.fields["email"], "Your e-mail")
        add_placeholder(self.fields["first_name"], "Ex.: Robert")
        add_placeholder(self.fields["last_name"], "Ex.: Rudi")

    password = forms.CharField(
        widget= forms.PasswordInput(attrs={
            "placeholder": "Your password"
        }),
        error_messages= {
            "required": "Password must not be empty"
        },
        help_text= (
            "Password must have at least one uppercase letter, one lowercase letter and one number. ",
            "The length should be at least 8 characters."
        ),
        validators= [strong_password]
    )

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Repeat your password"
    }))

    

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        # exclude = ["username"]
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "E-mail",
            "password": "Password"
        }
        help_texts = {
            "email": "The e-mail must be valid"
        }
        error_messages = {
            "username": {
                "required": "This field must be required"
            }
        }
        widgets = {
            "first_name": forms.TextInput(attrs= {
                "placeholder": "Type your username here", 
                "class": "text-input"
            }),
            "password": forms.PasswordInput(attrs= {
                "placeholder": "Type your password here"
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            password_error = ValidationError(
                    "Password and password2 must be equal",
                    code="invalid"
                )
            raise ValidationError({
                "password" : password_error,
                "password2" : password_error
            })
    