from work_log.journal.models import Item
from django.test import TestCase


class HomePageTest(TestCase):
    """ Тест домашней страницы. """

    def test_uses_home_template(self):
        """ Тест: используется домашний шаблон. """
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'index.html')

    def test_only_saves_items_when_necessary(self):
        """ Тест: сохраняет элемент, только когда нужно. """
        response = self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        """ Тест: можно сохранить post-запрос. """
        self.client.post("/",  data={"item_text": "Я ничего не делал"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "Я ничего не делал")

    def test_redirects_after_POST(self):
        """ Тест: переадресует после post-запроса. """
        response = self.client.post(
            "/",
            data={"item_text": "Я ничего не делал"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_display_all_list_items(self):
        """ Тест: отображаются все элементы списка. """
        Item.objects.create(text="Элемент 1")
        Item.objects.create(text="Элемент 2")
        response = self.client.get('/')
        self.assertIn("Элемент 1", response.content.decode())
        self.assertIn("Элемент 2", response.content.decode())


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
