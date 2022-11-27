from work_log.journal.models import Item
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


class RecordModelTest(TestCase):
    """ Тест модели элемента записи. """

    def test_saving_and_retrieving_items(self):
        """ Тест: сохранения и получения элементов списка. """
        first_item = Item()
        first_item.text = "Я сделал то-то..."
        first_item.save()

        second_item = Item()
        second_item.text = "Что-то делал ..."
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "Я сделал то-то...")
        self.assertEqual(second_saved_item.text, "Что-то делал ...")
