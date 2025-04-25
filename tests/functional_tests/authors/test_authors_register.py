from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsRegisterTest(AuthorsBaseTest):
    def get_by_id(self, web_element, id):
        return web_element.find_element(
            By.XPATH,
            id
        )


    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)


    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form"
        )


    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, "email").send_keys("email@email.com")

        callback(form)
        return form


    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_id(form, "//input[@id='id_first_name']")
            first_name_field.send_keys(" ")
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn("Write your first name", form.text)
        self.form_field_test_with_callback(callback)


    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_id(form, "//input[@id='id_last_name']")
            last_name_field.send_keys(" ")
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn("Write your last name", form.text)
        self.form_field_test_with_callback(callback)


    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_id(form, "//input[@id='id_username']")
            username_field.send_keys(" ")
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn(
                "This field must not be empty", 
                form.text
            )
        self.form_field_test_with_callback(callback)


    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_id(form, "//input[@id='id_email']")
            email_field.send_keys("email@invalid")
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn(
                "The e-mail must be valid", 
                form.text
            )
        self.form_field_test_with_callback(callback)


    def test_passwords_do_not_match(self):
        def callback(form):
            password1_field = self.get_by_id(form, "//input[@id='id_password']")
            password2_field = self.get_by_id(form, "//input[@id='id_password2']")
            password1_field.send_keys("P@ssw0rd")
            password2_field.send_keys("P@ssw0rd_Different")
            password2_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn(
                "Password and password2 must be equal", 
                form.text
            )
        self.form_field_test_with_callback(callback)

    
    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        self.get_by_id(form, "//input[@id='id_first_name']").send_keys("First Name")
        self.get_by_id(form, "//input[@id='id_last_name']").send_keys("Last Name")
        self.get_by_id(form, "//input[@id='id_username']").send_keys("my_username")
        self.get_by_id(form, "//input[@id='id_email']").send_keys("email@valid.com")
        self.get_by_id(form, "//input[@id='id_password']").send_keys("P@ssw0rd")
        self.get_by_id(form, "//input[@id='id_password2']").send_keys("P@ssw0rd")

        form.submit()

        self.assertIn(
            "Your user is created, please login",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
