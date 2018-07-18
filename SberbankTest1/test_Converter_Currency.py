from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import xml.etree.cElementTree as ET
import pytest
import allure

xml_file = ("ConverterCurrency.xml")
tree = ET.ElementTree(file=xml_file)

@allure.story('Тест выбора валюты')
class TestCurrency:

    @allure.title('Тест выбора валюты')
    @pytest.mark.parametrize('exchange', (tree.findall('Currency')))
    def test_converter_exchange(self, driver, exchange):
        wait = WebDriverWait(driver, 10)

        # Текст для проверки обменной и получаемой валюты
        check1 = exchange.find('Check1').text
        check2 = exchange.find('Check2').text
        action_chains = ActionChains(driver)

        with pytest.allure.step(check1 + ', ' + check2):

            # XPATH для выбора валют во всплывающих окнах
            first_choice = exchange.find('FirstChoice').text
            second_сhoice = exchange.find('SecondСhoice').text

            with pytest.allure.step('Открыть http://www.sberbank.ru/ru/quotes/converter'):
                driver.get('http://www.sberbank.ru/ru/quotes/converter')

            with pytest.allure.step('Клик по верхней валюте'):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[1]/div/div[2]/div/div[1]/div[3]/div[2]/div/header/em') ) )\
                    .click()

            with pytest.allure.step('Выбор валюты на обмен'):
                wait.until(EC.element_to_be_clickable((By.XPATH,  first_choice))).click()

            with pytest.allure.step('Закрыть уведомление о cookie, мешающее клику по нижней валюте'):
                try:
                    action_chains.click(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div/table/tbody/tr/td/div/div/div/div/div/div[3]/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div[3]/a' ) ) \
                        .perform ()
                except:
                    print('no_cookies')

            with pytest.allure.step('Клик по нижней валюте'):

                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[1]/div/div[2]/div/div[1]/div[4]/div[2]/div/header/em') ) )\
                    .click()

            with pytest.allure.step('Выбор получаемой валюты'):
                wait.until(EC.element_to_be_clickable((By.XPATH, second_сhoice))).click()

            # Необходимо из-за особенностей отображения.
            with pytest.allure.step('Проверка валюты на обмен в окне курса'):

                # Первая валюта - RUB, проверка
                if check1 == 'RUB':
                    assert wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[2]/td[1]')))\
                           .get_attribute("textContent") == check2 + ' / RUB'

                # Вторая валюта - RUB, проверка.
                elif check2 == 'RUB':
                    assert wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[2]/td[1]' ))) \
                               .get_attribute("textContent") == check1 + ' / RUB'

                # Ни одна валюта не RUB, проверка двух значений.
                else:
                    assert wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[2]/td[1]' ))) \
                               .get_attribute("textContent") == check1 + ' / RUB'
                    assert wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[3]/td[1]'))) \
                               .get_attribute("textContent") == check2 + ' / RUB'

            with pytest.allure.step('Двойной клик в поле ввода'):
                action_chains.double_click(driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input')).perform()

            with pytest.allure.step('Ввод числа 100, Enter'):
                action_chains.send_keys('100', Keys.ENTER).perform()

            with pytest.allure.step('Проверка валюты в "Чеке"'):

                # Валюта на обмен
                assert (check1 in wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[2]/div/span[2]') ) )\
                        .text)
                # Полученная валюта
                assert (check2 in driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[2]/div/span[3]')
                        .text)
