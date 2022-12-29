# scheduler_tasks
Cкрипты для запуска в Планировщике заданий Windows

## the_bat
Покакой-то причине переодически слетает возможность отправить по почте файл из контекстного меню проводника Отправить -> Адресат. Опытным путем было выяснено, что это происходит из-за того что в реестре HKEY_LOCAL_MACHINE\SOFTWARE\Clients\Mail вместо строки "The Bat!" меняется на что-то с Outlook. Посему решил сделать скрипт который смотрит что там и если не то, что надо - меняет на нужное.  
> Попутно выяснил как сделать регулярно выполняющуюся задачу :) под Windows 10 - как оказалось нужно делать задачу которая выполняется **однократно**, и задать ей регулярность повторов.

**the_bat.bat** - ❗ Указывается путь до экзешника питона из виртуального окружения проекта

```
d:\programming\pyProjects\py_utils\venv\Scripts\pythonw.exe d:\programming\pyProjects\py_utils\scheduler_tasks\the_bat.pyw
```

**the_bat.pyw** - расширение .pyw чтоб консоль не вылазила  
**the_bat_functioned.py** - версия с декомпозицей на кучку функций

### Скрины из Планировщика
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/scheduler_tasks/img/the_bat_01_общие.png?raw=true "Владка Общие")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/scheduler_tasks/img/the_bat_02_триггеры.png?raw=true "Вкладка Триггеры")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/scheduler_tasks/img/the_bat_03_действия.png?raw=true "Вкладка Действия")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/scheduler_tasks/img/the_bat_04_условия.png?raw=true "Вкладка Условия")
![alt-текст](https://github.com/i-dea-by/py_utils/blob/master/scheduler_tasks/img/the_bat_05_параметры.png?raw=true "Вкладка Параметры")
