from django.test import TestCase
from project.authors.forms import RegisterForm
from parameterized import parameterized

class AuthorRegisterFormUnittest(TestCase):
    @parameterized.expand([
        ("username", "Your username"),
        ("email", "Your e-mail"),
        ("first_name", "Ex.: Robert"),
        ("last_name", "Ex.: Rudi"),
        ("password", "Type your password"),
        ("password2", "Repeat your password")
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)


    @parameterized.expand([
        ("email", "The e-mail must be valid"),
        ("password", ("Password must have at least one uppercase letter, "
            "one lowercase letter and one number. "
            "The length should be at least 8 characters."))
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)


    @parameterized.expand([
        ("username", "Username"),
        ("email", "E-mail"),
        ("first_name", "First Name"),
        ("last_name", "Last Name"),
        ("password", "Password"),
        ("password2", "Password2")
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)
    

    