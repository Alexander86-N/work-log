from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    """Тест нового посетителя."""

    def setUp(self):
        """Установка."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Демонтаж."""
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """ подтверждение строки в таблице списка """
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест может начать список и получить его позже."""
        self.browser.get("http://localhost:8000")
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
        time.sleep(1)
        self.check_for_row_in_list_table("1: Кювета(синяя)-1980 шт.")

        # Текстовое поле предлагает записать ещё работу
        # Он вводит "Шпатель гладкий(оранж)-1700 шт."
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Шпатель гладкий(оранж)-1700 шт.")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        self.check_for_row_in_list_table("1: Кювета(синяя)-1980 шт.")
        self.check_for_row_in_list_table("2: Шпатель гладкий(оранж)-1700 шт.")
        # Страница снова обнавляется, и теперь показывает оба элемента списка
        # Сотруднику интересно. запомнит ли сайт записаную работу. Он видит. что
        # сайт сгенерировал для нго уникальный URL-адрес - об этом
        # выводится небольшое текстовое сообщение
        self.fail("Закончить тест!")
        # Он посещает этот URL-адрес - записаная работа там
        # Довольный он ваходит из приложения


if __name__ == "__main__":
    unittest.main(warnings="ignore")
