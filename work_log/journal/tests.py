from work_log.journal.models import Item, List
from django.test import TestCase


class HomePageTest(TestCase):
    """ Тест домашней страницы. """

    def test_uses_home_template(self):
        """ Тест: используется домашний шаблон. """
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'index.html')


class ListAndItamModelsTest(TestCase):
    """ Тест модели элемента записи. """

    def test_saving_and_retrieving_items(self):
        """ Тест: сохранения и получения элементов списка. """
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "Я сделал то-то..."
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Что-то делал ..."
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "Я сделал то-то...")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Что-то делал ...")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    """ Тест представления списка """

    def test_uses_list_template(self):
        """ Тест: использование шаблона списка. """
        response = self.client.get("/lists/new_url/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_items(self):
        """ Тест: отображаются все элементы списка. """
        list_ = List.objects.create()
        Item.objects.create(text="Элемент 1", list=list_)
        Item.objects.create(text="Элемент 2", list=list_)

        response = self.client.get('/lists/new_url/')

        self.assertContains(response, "Элемент 1")
        self.assertContains(response, "Элемент 2")


class NewListTest(TestCase):
    """ Тест нового списка. """

    def test_can_save_a_POST_request(self):
        """ Тест: можно сохранить post-запрос. """
        self.client.post("/lists/new",  
                         data={"item_text": "Я первый раз записываюсь."})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "Я первый раз записываюсь.")

    def test_redirects_after_POST(self):
        """ Тест: переадресует после post-запроса. """
        response = self.client.post("/lists/new",
                                    data={"item_text": "Я ничего не делал"})
        self.assertRedirects(response, "/lists/new_url/")
