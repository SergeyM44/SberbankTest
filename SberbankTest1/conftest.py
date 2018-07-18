import pytest


@pytest.fixture(params=["Chrome", "Firefox"],scope="session")
def driver(request):
    from selenium import webdriver

    # Операции будут выполняться в двух браузерах
    # В данную директорию нужно поместить chromedriver.exe и geckodriver.exe
    if request.param == "Chrome":
        web_driver = webdriver.Chrome(executable_path=r'C:\drivers\chromedriver.exe')
    if request.param == "Firefox":
        web_driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe')

    # Раскрывает окно браузера, можно сменить на minimize
    web_driver.maximize_window ()

    # Закрытие браузера после завершения тестов
    request.addfinalizer(web_driver.quit)

    return web_driver
