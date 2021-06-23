# Урок №5  курса ["API веб-сервисов"](https://dvmn.org/modules/web-api/). 

Настоящий проект позволяет провести сравнение среднего уровня заработной платы для разработчиков в Москве.


Проект использует следуюшие Api:
1. [Api hh.ru](https://github.com/hhru/api);
2. [Api SuperJob.ru](https://api.superjob.ru/);
Для работы с [Api SuperJob.ru](https://api.superjob.ru/) необходимо пройти регистрацию и получить token доступа.


Библиотеки используемые в проекте:

* [Библиотека requests](https://requests.readthedocs.io/en/master/user/install/#install);
* [Библиотека python-dotenv](https://pypi.org/project/python-dotenv/);
* [Библиотека terminaltables](https://github.com/Robpol86/terminaltables).


Состав проекта:
1. [main.py](https://github.com/ArtsAnton/devman_hw/tree/main/api/les_5/main.py) - основной файл;
2. [settings.py](https://github.com/ArtsAnton/devman_hw/tree/main/api/les_5/settings.py) - файл содержащий информацию для запросов (headers, payload и т.д).

Начало работы:
1. Подготовка к работе;

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt 
```
2. Запуск проекта;
```
python3 main.py
```

3. Пример работы кода.

![table](https://github.com/ArtsAnton/devman_hw/blob/main/api/les_5/img/table.png)

### Цель проекта

Код написан в образовательных целях в рамках выполнения урока № 5 онлайн-курса для веб-разработчиков [devmn.org](https://dvmn.org/modules/).