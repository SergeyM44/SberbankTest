import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

class PageObjects:
    # Поле ввода калькулятора валют
    converter_insert_field = 'form input'

    # Получаемая сумма в чеке
    converter_result_money = 'aside .rates-converter-result'

    # Поле выбора меняемой валюты
    converter_upper_curency = '.rates-aside__filter-block-line_field_converter-from em'

    # Поле выбора получаемой валюты
    converter_lower_curency = 'div:nth-child(4) em'

    # Закрывающий крест окна cookie
    converter_cookie_close = 'div.kitt-col.kitt-col_xs_1  a'

    # Табло валют (USD/RUB или другое)
    converter_first_currency_exchange = 'tr:nth-child(2)  .rates-current__table-cell_column_name'

    # Второе табло валют (USD/RUB или другое, появляется при обмене одной иностранной валюты на другую)
    converter_second_currency_exchange = 'tr:nth-child(3)  .rates-current__table-cell_column_name'

    # Валюта на обмен в чеке
    converter_give_currency = '.rates-converter-result__total .rates-converter-result__total-from'

    # Получаемая валюта в чеке
    converter_get_currency = '.rates-converter-result__total .rates-converter-result__total-to'

    # Цена продажи валюты на обмен
    converter_upper_currency_sell = 'tr:nth-child(2)  .rates-current__table-cell_column_sell .rates-current__rate-value'

    # Цена покупки валюты на обмен
    converter_upper_currency_buy = 'tr:nth-child(2) .rates-current__table-cell_column_buy .rates-current__rate-value'

    # Цена продажи получаемой валюты
    converter_lower_currency_sell = 'tr:nth-child(3) .rates-current__table-cell_column_sell .rates-current__rate-value'


class SberLinks:
    # Страница калькулятора валют
    converter_link = 'http://www.sberbank.ru/ru/quotes/converter'


@pytest.fixture(params=["Chrome", "Firefox"],scope="session")
def driver(request):
    # Операции будут выполняться в двух браузерах
    # Относительный путь
    if request.param == "Chrome":
        web_driver = webdriver.Chrome('\drivers\chromedriver')

    elif request.param == "Firefox":
        web_driver = webdriver.Firefox(executable_path=r'\drivers\geckodriver')

    # Раскрывает окно браузера, можно сменить на minimize
    web_driver.maximize_window()

    # Закрытие браузера после завершения тестов
    request.addfinalizer(web_driver.quit)

    return web_driver


@pytest.fixture ()
def wait(driver):
    wait = WebDriverWait(driver, 5)
    return wait


# number_to_input(ДАННЫЕ, КОТОРЫЕ НУЖНО ВВЕСТИ В ПОЛЕ ВВОДА КАЛЬКУЛЯТОРА ВАЛЮТ)
@pytest.fixture()
def number_to_input(driver, wait):
    def _input_action(input_data):

        with pytest.allure.step ( 'Двойной клик в поле ввода' ):
            ActionChains ( driver ).double_click (
                wait.until ( EC.element_to_be_clickable ( (By.CSS_SELECTOR, PageObjects.converter_insert_field) ) ) ).perform ()

        with pytest.allure.step ( 'Ввод: ' + input_data + ', Enter' ):
            ActionChains ( driver ).send_keys (Keys.BACKSPACE*15, input_data, Keys.ENTER ).perform ()
    return _input_action


@pytest.fixture (scope="function")
def converter_page(driver):
   converter_get = driver.get(SberLinks.converter_link)
   return converter_get


# @pytest.fixture()
# def wait_until(wait):
#     def __wait_until(input_data):
#         wait.until ( EC.element_to_be_clickable ( (By.CSS_SELECTOR, input_data) ) )
#     return __wait_until
