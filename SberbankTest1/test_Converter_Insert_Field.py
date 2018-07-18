from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import xml.etree.cElementTree as ET
import pytest
import allure

# Файл для параметризации в директории проекта
xml_file = ("ConverterValues.xml")
tree = ET.ElementTree(file=xml_file)


@allure.story('Тест строки ввода калькулятора валют')
class TestField:

    @allure.title("Корректные данные" )
    @pytest.mark.parametrize('numbers', (tree.findall('numbers')))
    # Драйвер взят из conftest.py
    def test_converter_numbers(self, driver, numbers):
        wait = WebDriverWait(driver, 10)

        # Данные для ввода и проверки
        input_number = numbers.find('inputnumber').text
        number_check = numbers.find('numbercheck').text

        # Имя теста
        with pytest.allure.step('Ввод числа:' + input_number):

            with pytest.allure.step('Открыть http://www.sberbank.ru/ru/quotes/converter'):
                driver.get('http://www.sberbank.ru/ru/quotes/converter')

            with pytest.allure.step('Проверка кликабельности поля ввода'):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input')))

            with pytest.allure.step('Двойной клик в поле ввода'):
                ActionChains(driver).double_click(driver.find_element_by_xpath ('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input' ) ).\
                    perform()

            with pytest.allure.step('Ввод числа: ' + input_number + ', Enter'):
                ActionChains(driver).send_keys(input_number, Keys.ENTER).perform()

            with pytest.allure.step('Проверка отображения "Чека"'):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[2]')))

            # Проверка отображения введённой суммы в чеке.
            with pytest.allure.step('Отображение строки: ' + number_check):
                assert (number_check in driver.find_element_by_tag_name('body').text)

            with pytest.allure.step('Наличие текста "Вы получите:"'):
                assert ('Вы получите:' in driver.find_element_by_tag_name('body').text)


    # Драйвер взят из conftest.py
    @allure.title("Некорректные данные")
    @pytest.mark.parametrize('strings', (tree.findall('strings')))
    # Драйвер взят из conftest.py
    def test_converter_string(self, driver, strings):
        wait = WebDriverWait(driver, 10)

        # Данные для ввода и название теста
        input_strings = strings.find('inputstring').text
        testname = strings.find('testname').text

        # Имя теста
        with pytest.allure.step(testname):

            with pytest.allure.step('Открыть http://www.sberbank.ru/ru/quotes/converter'):
                driver.get('http://www.sberbank.ru/ru/quotes/converter')

            with pytest.allure.step('Проверка кликабельности поля ввода'):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input')))

            with pytest.allure.step('Двойной клик в поле ввода'):
                ActionChains(driver).double_click(driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input'))\
                    .perform()

            # Ввод данных, Enter
            with pytest.allure.step(testname + ', Enter'):
                ActionChains(driver).send_keys(input_strings, Keys.ENTER).perform()

            with pytest.allure.step('Значение поля ввода не изменилось'):
                assert driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input').get_attribute("value") == ''
