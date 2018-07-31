from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.cElementTree as ET
import pytest
import allure
from conftest import PageObjects

# Файл для параметризации в директории проекта
tree = ET.ElementTree(file="ConverterCurrency.xml")


@allure.story('Тест формулы конвертации валют')
class TestFormula:

    @allure.title('Тест формулы конвертации валют')
    @pytest.mark.parametrize('exchange', (tree.findall('Currency')))
    # Драйвер взят из conftest.py
    def test_converter_formula(self, driver, exchange, number_to_input, wait, converter_page):
        check1 = exchange.find('Check1').text
        check2 = exchange.find('Check2').text

        with pytest.allure.step(check1 + ' в ' + check2):

            # Selector для выбора валют во всплывающих окнах
            first_choice = (exchange.find ( 'FirstChoice' ).text)
            second_choice = (exchange.find ( 'SecondChoice' ).text)

            with pytest.allure.step('Клик по верхней валюте'):
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_upper_curency))).click()

            with pytest.allure.step('Выбор валюты на обмен'):
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,  first_choice))).click()

            with pytest.allure.step('Клик по нижней валюте'):
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_lower_curency) ) )\
                    .click()

            with pytest.allure.step('Выбор получаемой валюты'):
                try:
                    wait.until ( EC.element_to_be_clickable ( (By.CSS_SELECTOR, second_choice) ) ).click ()
                except:
                    with pytest.allure.step ( 'Закрыть мешающее уведомление, выюрать валюту валюту' ):
                        driver.find_element_by_css_selector ( PageObjects.converter_cookie_close ).click ()
                        wait.until ( EC.invisibility_of_element_located ((By.CSS_SELECTOR, PageObjects.converter_cookie_close) ) )
                        wait.until ( EC.element_to_be_clickable ((By.CSS_SELECTOR, PageObjects.converter_lower_curency) ) ).click ()
                        wait.until ( EC.element_to_be_clickable ( (By.CSS_SELECTOR, second_choice) ) ).click ()

            with pytest.allure.step('Проверка расчёта в "чеке"'):

                # Если меняемая валюта - рубль
                if check1 == 'RUB':

                    # Клик в поле ввода, ввод текущего курса покупаемой валюты к рублю, на выходе ожадается 1,00
                    number_to_input((wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_upper_currency_sell )))).get_attribute("textContent"))

                    # Проверка чека на наличие строки "1,00"
                    assert '1,00' in ((wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_get_currency )))).get_attribute("textContent"))

                # Если получаемая валюта - рубль
                elif check2 == 'RUB':

                    # Клик в поле ввода, ввод - 1 единица иностранной валюты
                    number_to_input('1')

                    # Проверка наличия в "чеке" текущего курса данной валюты
                    assert (wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_upper_currency_buy)))).get_attribute("textContent" )\
                        in (wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_get_currency)))).get_attribute("textContent")

                # Если ни одна из валют не рубль
                else:
                    # Ввод числа 1, Enter
                    number_to_input('1')

                    # Курс покупки первой валюты делим на курс продажи второй валюты
                    xx = float((wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_upper_currency_buy))).get_attribute("textContent" )).replace(',', '.' ))

                    yy = float((wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_lower_currency_sell))).get_attribute("textContent")).replace(',', '.' ) )

                    zz = str(round((xx / yy), 2)).replace('.', ',')

                    # Ищем полученный результат в "Чеке"
                    assert zz in ((wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_get_currency)))).get_attribute("textContent"))
