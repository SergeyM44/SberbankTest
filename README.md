Тестовое задание - Python:
WebDriver

Придумать сценарии для тестирования Калькулятора иностранных валют на сайте http://www.sberbank.ru/ru/quotes/converter
Автоматизировать из них 3 сценария 

Результат выполненного ТЗ:

Реализовать функциональные (pytest) тесты сценариев.
Использовать инструмент Selenium WebDriver
Каждый тест должен выглядеть в отчете как отдельный тестовый сценарий
Тест должны быть параметризирован в XML или CSV
Результатом выполнения должен быть Yandex.Allure отчет
Исходный код проекта должен быть выложен на github или bitbucket.


_______________________________________________________________________


Тест кейсы https://docs.google.com/spreadsheets/d/150OI9MsFb8YRldY5hMHB3iJo2ev_pFqXDIRnzPcGocI/edit#gid=1225610413

Тест-кейсы в отчёте Allure сгруппированы на вкладке "Функциональность".


Несколько замечаний, которые без чёткого знания ТЗ создателей проекта не могу определить как баги:
1. При клике в поле вввода калькулатора, заранее введённые данные (100) не выделяются, что вынуждает пользователя сначала удалять старые данные.

2. Неясно, почему калькулятор не принимает числа менее единицы. Возможно мелочь не разменивают. Тем не менее, хотя "чек" не отображается, значение элемента принимает ноль и числа меньше единицы, что будет видно в отчёте как ошибки.

3. Для многих валют в течении нескольких дней отсутствуют котировки, даже неактуальные. Не вникая глубоко в дела сбербанка, трудно сказать, с чем это связано. Возможно, в это время данной валюты недостаточно для торговли. Чтобы не заводить багов понапрасну, предлагаю тестить связки "рубль-евро", "рубль-доллар", "евро-рубль", "доллар-рубль", "евро-доллар", "доллар-евро".

4. Я не писал тест-кейс на таблицу курсов, так как не совсем понятно, что там должно отображаться. Диапазон дат не соответствует выбранному, параметры Сумма от: и Сумма до: - всегда 0 и 9999999999.99 соответственно. 

5. Без обновления страницы на каждом тесте возникают баги поля ввода. В случае их устранения достаточно будет изменить scope фикстуры driver на class.
