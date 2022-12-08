from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя."""

    def setUp(self):
        """Установка."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Демонтаж."""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """ Ожидать строку в таблице списка """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест может начать список и получить его позже."""
        self.browser.get(self.live_server_url)
        # Страница имеет заголовок
        self.assertIn("Рабочий журнал", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Рабочий журнал", header_text)
        # Сотруднику предлагается ввести проделаную работу
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"),
                         "Записать результаты")
        # Он набирает в текстовом поле "Кювета(синяя)-1980 шт."
        inputbox.send_keys("Кювета(синяя)-1980 шт.")
        # Когда он нажимает 'ENTER', страница обновляется, и теперь содержит
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Кювета(синяя)-1980 шт.")

        # Текстовое поле предлагает записать ещё работу
        # Он вводит "Шпатель гладкий(оранж)-1700 шт."
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Шпатель гладкий(оранж)-1700 шт.")
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table("1: Кювета(синяя)-1980 шт.")
        self.wait_for_row_in_list_table("2: Шпатель гладкий(оранж)-1700 шт.")
        # Страница снова обнавляется, и теперь показывает оба элемента списка
        # Сотруднику интересно. запомнит ли сайт записаную работу. Он видит. что
        # сайт сгенерировал для нго уникальный URL-адрес - об этом
        # выводится небольшое текстовое сообщение
#        self.fail("Закончить тест!")
        # Он посещает этот URL-адрес - записаная работа там
        # Довольный он ваходит из приложения

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """ Тест: разные пользователи могут начинать списки по разным url. """
        # Сотрудник хочет записать задание
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Банка 1,5 л(желтая)-1800 шт.")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Банка 1,5 л(желтая)-1800 шт.")
        # Он замечает, что его список имеет уникальный URL-адрес
        first_list_url = self.browser.current_url
        self.assertRegex(first_list_url, "/lists/.+")

        # Теперь другой сотрудник хочет записаться
        
        ## Мы используем новый сеанс браузера,тем самым обеспечиваея, чтобы
        ## никакая информация от первого сотрудника не прошла через данные cookie
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # Сотрудник посещает домашнюю страницу. Нет признаков первого сотрудника
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Банка 1,5 л(желтая)-1800 шт.", page_text)
        self.assertNotIn("Шпатель гладкий(оранж)-1700 шт.", page_text)
        # Сотрудник начинае записывать свою работу
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Ванночка(черная)-1620 шт.")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Ванночка(черная)-1620 шт.")
        # Сотрудник получает уникальный URL-адрес
        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, "/lists/.+")
        self.assertNotEqual(second_list_url, first_list_url)
        # Опять нет следа от списка первого сотрудника
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Банка 1,5 л(желтая)-1800 шт.", page_text)
        self.assertIn("Ванночка(черная)-1620 шт.", page_text)
