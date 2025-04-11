from django.test import TestCase
from project.authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

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
    


class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@email.com",
            "password": "Str0ngP@ssword1",
            "password2": "Str0ngP@ssword1",
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ("username", "This field must not be empty")
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("UTF-8"))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = "Username must have at least 4 characters"
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less then 150 characters'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))


    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = "abc123"
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be "
            "at least 8 characters."  
        )
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = "@Abcabc123"
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.context['form'].errors.get('password'))


    def test_password_is_password_confirmation_are_equal(self):
        self.form_data['password'] = "@Abcabc123"
        self.form_data['password2'] = "@Abcabc1234"
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = "Password and password2 must be equal"
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = "@Abcabc123"
        self.form_data['password2'] = "@Abcabc123"
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
            url = reverse('authors:create')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        msg = "User email is already in use"

        self.assertIn(msg, response.context["form"].errors.get("email"))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:create')
        self.form_data.update({
            "username": "testuser",
            "password": "@Bc12345678",
            "password2": "@Bc12345678"
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username = "testuser",
            password = "@Bc12345678"
        )

        self.assertTrue(is_authenticated)
        