from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import xml.etree.cElementTree as ET
import pytest
import allure


# Файл для параметризации в директории проекта
xml_file = ("ConverterCurrency.xml")
tree = ET.ElementTree(file=xml_file)


@allure.story('Тест формулы конвертации валют')
class TestFormula:

    @allure.title('Тест формулы конвертации валют')
    @pytest.mark.parametrize('exchange', (tree.findall('Currency')))
    # Драйвер взят из conftest.py
    def test_converter_formula(self, driver, exchange):
        wait = WebDriverWait(driver, 10)
        check1 = exchange.find('Check1').text
        check2 = exchange.find('Check2').text

        with pytest.allure.step(check1 + ', ' + check2):

            # XPATH для выбора валют во всплывающих окнах
            first_choice = (exchange.find ( 'FirstChoice' ).text)
            second_choice = (exchange.find ( 'SecondСhoice' ).text)


            with pytest.allure.step('Открыть http://www.sberbank.ru/ru/quotes/converter'):
                driver.get('http://www.sberbank.ru/ru/quotes/converter')

            with pytest.allure.step('Клик по верхней валюте'):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[1]/div/div[2]/div/div[1]/div[3]/div[2]/div/header/em') ) )\
                    .click()

            with pytest.allure.step('Выбор валюты на обмен'):
                wait.until(EC.element_to_be_clickable((By.XPATH,  first_choice))).click()

            with pytest.allure.step('Закрыть уведомление о cookie, мешающее клику по нижней валюте'):
                try:
                    ActionChains(driver).click(driver.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div/table/tbody/tr/td/div/div/div/div/div/div[3]/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div[3]/a' ) ) \
                        .perform()
                except:
                    print('no cookie')

            with pytest.allure.step('Клик по нижней валюте'):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[1]/div/div[2]/div/div[1]/div[4]/div[2]/div/header/em') ) )\
                    .click()

            with pytest.allure.step('Выбор получаемой валюты'):
                wait.until(EC.element_to_be_clickable((By.XPATH, second_choice) ) ).click()

            with pytest.allure.step('Проверка расчёта в "чеке"'):

                # Если меняемая валюта - рубль
                if(((wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[3]/div[2]/div/header/strong' ))))
                            .get_attribute("textContent") == 'RUB')):


                    # Клик в поле ввода, ввод текущего курса покупаемой валюты к рублю, на выходе ожадается 1,00
                    ActionChains(driver).double_click(driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input' ) )\
                        .perform()
                    ActionChains(driver).send_keys(driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[2]/td[3]/span/span[1]' ) \
                           .get_attribute("textContent"), Keys.ENTER).perform()

                    # Проверка чека на наличие строки "1,00"
                    assert '1,00' in (((wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[2]/div/span[3]' ))))
                        .get_attribute("textContent")))

                # Если получаемая валюта - рубль
                elif((wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[4]/div[2]/div/header/strong' ))))
                            .get_attribute("textContent") == 'RUB'):

                    # Клик в поле ввода, ввод - 1 единица иностранной валюты
                    ActionChains(driver).double_click(driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input' ) )\
                        .perform()
                    ActionChains(driver).send_keys('1', Keys.ENTER).perform()

                    # Проверка наличия в "чеке" текущего курса данной валюты
                    assert (driver.find_element_by_xpath(
                    '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[2]/td[2]/span/span[1]' ) \
                           .get_attribute("textContent")) in (((wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[2]/div/span[3]' ))))
                        .get_attribute("textContent")))

                # Если ни одна из валют не рубль
                else:
                    # Ввод числа 1, Enter
                    ActionChains(driver).double_click(driver.find_element_by_xpath(
                        '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div/div/div[2]/div/div[1]/div[2]/div/form/input' ) ).perform ()
                    ActionChains(driver).send_keys('1', Keys.ENTER).perform()

                    # Курс покупки первой валюты делим на курс продажи второй валюты
                    xx = float ( (driver.find_element_by_xpath('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[2]/td[2]/span/span[1]' ) \
                       .get_attribute("textContent" )).replace(',', '.' ) )
                    yy = float((driver.find_element_by_xpath ('//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/table/tbody/tr[3]/td[3]/span/span[1]' ) \
                                        .get_attribute("textContent" )).replace ( ',', '.' ) )
                    zz = str(round((xx / yy), 1)).replace('.', ',')

                    # Ищем полученный результат в "Чеке"
                    assert zz in (((wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/table/tbody/tr/td/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/aside/div/div[2]/div[1]/span[3]' ))))
                    .get_attribute("textContent")))


