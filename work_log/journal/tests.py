from django.test import TestCase


class HomePageTest(TestCase):
    """ Тест домашней страницы. """

    def test_uses_home_template(self):
        """ Тест: используется домашний шаблон. """
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'index.html')

    def test_can_save_POST_request(self):
        """ Тест: можно сохранить post-запрос. """
        response = self.client.post(
            "/", 
            data={"item_text": "Я ничего не делал"}
        )
        self.assertIn("Я ничего не делал", response.content.decode())
        self.assertTemplateUsed(response, 'index.html')
