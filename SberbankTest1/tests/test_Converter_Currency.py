from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.cElementTree as ET
import pytest
import allure
from conftest import PageObjects

# Файл для параметризации в директории проекта
tree = ET.ElementTree(file="ConverterCurrency.xml")

@allure.story('Тест выбора валюты')
class TestCurrency:
    @allure.title('Тест выбора валюты')
    @pytest.mark.parametrize('exchange', (tree.findall('Currency')))
    def test_converter_exchange(self, driver, exchange, number_to_input, wait, converter_page):

        failure_log = []

        # Текст для проверки обменной и получаемой валюты
        check1 = exchange.find('Check1').text
        check2 = exchange.find('Check2').text

        with pytest.allure.step(check1 + ' в ' + check2):

            # Selector для выбора валют во всплывающих окнах
            first_choice = exchange.find('FirstChoice').text
            second_choice = exchange.find('SecondChoice').text

            with pytest.allure.step('Клик по верхней валюте'):
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_upper_curency))).click()

            with pytest.allure.step('Выбор валюты на обмен'):
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,  first_choice))).click()

            with pytest.allure.step('Клик по нижней валюте'):
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_lower_curency) ) )\
                    .click()

            with pytest.allure.step ( 'Выбор получаемой валюты' ):
                try:
                    wait.until(EC.element_to_be_clickable ( (By.CSS_SELECTOR, second_choice) ) ).click ()
                except:
                    with pytest.allure.step ( 'Закрыть мешающее уведомление, выюрать валюту валюту' ):
                        driver.find_element_by_css_selector ( PageObjects.converter_cookie_close ).click ()
                        wait.until ( EC.invisibility_of_element_located( (By.CSS_SELECTOR, PageObjects.converter_cookie_close) ) )
                        wait.until (EC.element_to_be_clickable ( (By.CSS_SELECTOR, PageObjects.converter_lower_curency) ) ).click ()
                        wait.until ( EC.element_to_be_clickable ( (By.CSS_SELECTOR, second_choice) ) ).click ()

            # Необходимо из-за особенностей отображения.
            with pytest.allure.step('Проверка валюты на обмен в окне курса'):

                # Первая валюта - RUB, проверка
                if check1 == 'RUB':
                    try:
                        assert wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_first_currency_exchange)))\
                                   .get_attribute("textContent") == check2 + ' / RUB'
                    except Exception as err:
                        with pytest.allure.step('Ошибка окна "Валюта": ' + check2 + '/RUB. Строка 58.'):
                            print('Строка 58: ' + str(err))
                            failure_log.append('Ошибка окна "Валюта": ' + check2 + '/RUB. Строка 58. ')

                # Вторая валюта - RUB, проверка.
                elif check2 == 'RUB':
                    try:
                        assert wait.until ( EC.element_to_be_clickable ( (By.CSS_SELECTOR, PageObjects.converter_first_currency_exchange) ) )\
                                   .get_attribute ( "textContent" ) == check1 + ' / RUB'
                    except Exception as err:
                        with pytest.allure.step('Ошибка окна "Валюта": ' + check1 + '/RUB. Строка 67.'):
                            print('Строка 67: ' + str(err))
                            failure_log.append('Ошибка окна "Валюта": ' + check1 + '/RUB. Строка 67. ')

                # Ни одна валюта не RUB, проверка двух значений.
                else:
                    try:
                        assert wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_first_currency_exchange ))) \
                               .get_attribute("textContent") == check1 + ' / RUB'
                    except Exception as err:
                        with pytest.allure.step ('Ошибка окна "Валюта": ' + check1 + '/RUB. Строка 78.'):
                            print ('Строка 78: ' + str(err))
                            failure_log.append ('Ошибка окна "Валюта": ' + check1 + '/RUB. Строка 78. ')
                    try:
                        assert wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PageObjects.converter_second_currency_exchange))) \
                               .get_attribute("textContent") == check2 + ' / RUB'
                    except Exception as err:
                        with pytest.allure.step('Ошибка окна "Валюта": ' + check2 + '/RUB. Строка 85.'):
                            print('Строка 85: ' + str(err))
                            failure_log.append('Ошибка окна "Валюта": ' + check2 + '/RUB. Строка 85. ')

            # Вводим 100 для вызова чека
            number_to_input('100')

            with pytest.allure.step ( 'Проверка валюты в "Чеке"' ):

                # Валюта на обмен, полученная валюта
                try:
                    assert check1 in (wait.until (EC.element_to_be_clickable ( (By.CSS_SELECTOR, PageObjects.converter_give_currency) ) ).text)
                except Exception as err:
                    with pytest.allure.step ('Ошибка: валюта на обмен в чеке' + check1 + '/RUB. Строка 99.'):
                        print('Строка 99: ' + str(err))
                        failure_log.append('Ошибка: валюта на обмен в чеке' + check1 + '/RUB. Строка 99. ')
                try:
                    assert check2 in (wait.until (EC.element_to_be_clickable ( (By.CSS_SELECTOR, PageObjects.converter_get_currency) ) ).text)
                except Exception as err:
                    with pytest.allure.step ('Ошибка: валюта на обмен в чеке' + check1 + '/RUB. Строка 105.'):
                        print ('Строка 105: ' + str(err))
                        failure_log.append ('Ошибка: полученная валюта в чеке' + check2 + '/RUB. Строка 105.')

                if len(failure_log) > 0:
                    with pytest.allure.step(str(failure_log)):
                        print(str(failure_log))
                        pytest.fail(str(failure_log))
