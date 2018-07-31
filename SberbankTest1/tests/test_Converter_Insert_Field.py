from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.cElementTree as ET
import pytest
import allure
from conftest import PageObjects

# Файл для параметризации в директории проекта
tree = ET.ElementTree(file="ConverterValues.xml")



@allure.story('Тест строки ввода калькулятора валют')
class TestField:

    @allure.title("Корректные данные" )
    @pytest.mark.parametrize('correct_data', (tree.findall('correct_data')))
    # Описание фикстур в Conftest
    def test_converter_correct_data(self, driver, wait, correct_data, number_to_input, converter_page):

        # Данные для ввода и проверки
        input_data = correct_data.find('input_data').text
        data_check = correct_data.find('data_check').text

        # Имя теста
        with pytest.allure.step('Ввод числа:' + input_data):

            number_to_input(input_data)

            # Проверка отображения введённой суммы в чеке.
            with pytest.allure.step('Отображение строки: ' + data_check + 'в чеке'):
                assert data_check in wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_result_money))).text

    # Драйвер взят из conftest.py
    @allure.title("Некорректные данные")
    @pytest.mark.parametrize('incorrect_data', (tree.findall('incorrect_data')))
    # Описание фикстур в Conftest
    def test_converter_string(self, driver, incorrect_data, number_to_input, converter_page, wait):

        # Данные для ввода и название теста
        input_data = incorrect_data.find('input_data').text
        test_name = incorrect_data.find('test_name').text

        # Имя теста
        with pytest.allure.step(test_name):

            number_to_input(input_data)

            with pytest.allure.step('Value поля ввода не изменилось'):
                assert wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_insert_field))).get_attribute("value") == ''
