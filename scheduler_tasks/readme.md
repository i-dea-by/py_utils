# scheduler_tasks
Cкрипты для запуска в Планировщике заданий Windows

### the_bat
Покакой-то причине переодически слетает возможность отправить по почте файл из контекстного меню проводника Отправить -> Адресат. Опытным путем было выяснено, что это происходит из-за того что в реестре HKEY_LOCAL_MACHINE\SOFTWARE\Clients\Mail вместо строки "The Bat!" меняется на что-то с Outlook. Посему решил сделать скрипт который смотрит что там и если не то, что надо - меняет на нужное.  
Попутно выяснил как сделать регулярно выполняющуюся задачу :)
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/ "Владка Общие")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/ "Вкладка Триггеры")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/ "Вкладка Действия")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/ "Вкладка Условия")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/ "Вкладка Параметры")