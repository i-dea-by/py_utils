
# uber_cost_by_year
Скрипт анализирует mbox-файл полученный из экспорта гугловой почты, ищет письма от Убера за указанный год и суммирует стоимость поездок взятых из тела письма

### requirements.txt
```
beautifulsoup4  
tqdm  
lxml
```

### Примеры результата работы
```
date:  : 2021-05-03 16:55:11 Mon
to:    : <mail>
from   : Uber <no-reply@support-uber.com>
subject: Uber – отчёт о поездке 3 мая 2021 г.
price  : 7.00
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
date:  : 2021-05-03 16:20:42 Mon
to:    : <mail>
from   : Uber <no-reply@support-uber.com>
subject: Uber – отчёт о поездке 3 мая 2021 г.
price  : 5.20
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
```
![alt-текст](https://github.com/i-dea-by/py_utils/tree/master/uber_cost_by_year/uber.gif "Working")