
# taxi_cost_by_year
Скрипт анализирует mbox-файл полученный из экспорта гугловой почты, ищет письма от Убера/Яндекса за указанный год и суммирует стоимость поездок взятых из тела письма

### Как получить файл .mbox:
* https://takeout.google.com/settings/takeout
* Выбрать только «Почта», можно уточнить что именно из ящика экспортировать нажав кнопку «Выбраны все данные почты»
* Потом Далее, выбрать когда и как получать экспорт и нажать «Создать экспорт»

### requirements.txt
```
beautifulsoup4  
tqdm  
```

### Примеры результата работы
Если `print_log=True`:  
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/taxi_cost_by_year/taxi_log.gif?raw=true "Working with log")  
Если `print_log=False`:  
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/taxi_cost_by_year/taxi.gif?raw=true "Working")

### История изменений:
#### 0.0.3 - 2023.01.01 
* Яндекс.Такси в html-е оказывается даёт json-строку с данными поездки   
#### 0.0.1 - 2023.01.01 
* C 23 года перешел на Яндекс.Такси. Для этого файл yandex.py. Для того, чтобы Яндекс начал присылать уведомления на почту нужно в приложении указать почту  
#### 0.0.0 - 2022.12.30 
* В 22 году  декабре, примерно, стали приходить глючные письма без данных, поэтому если нету, тогда 0