# Урок №6  курса ["API веб-сервисов"](https://dvmn.org/modules/web-api/)

Настоящий проект позволяет автоматизировать процесс публикации новых записей в группах социальной сети [vk.com](https://vk.com).


Проект использует следующие Api:
1. [Хkcd.com](https://xkcd.com/json.html) - контент для загрузки;
2. [Api vk.com](https://vk.com/dev).

Для работы с [vk.com](https://vk.com) Вам необходимо получить [token](https://vk.com/dev/implicit_flow_user) доступа и зарегистрировать группу в [vk.com](https://vk.com),
а также создать файл .env для хранения этих переменных.
Содержимое файла .env:
   ```
   VK_GROUP='...'
   VK_TOKEN='...'
   ```

Процесс получения токена доступа изложен в [документации](https://vk.com/dev/implicit_flow_user). Запрос токена должен проводиться с учетом следующего:
1. параметр scope должен содержать следующие права доступа - scope=photos,groups,wall,offline;
2. параметр redirect_uri передавать не надо.
    
Библиотеки используемые в проекте:

* [Библиотека requests](https://requests.readthedocs.io/en/master/user/install/#install);
* [Библиотека python-dotenv](https://pypi.org/project/python-dotenv/).


Состав проекта:
1. [main.py](https://github.com/ArtsAnton/devman_hw/tree/main/api/les_6/main.py) - основной файл;
2. [requirements.txt ](https://github.com/ArtsAnton/devman_hw/tree/main/api/les_6/requirements.txt) - зависимости.

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

### Цель проекта

Код написан в образовательных целях в рамках выполнения урока № 6 онлайн-курса для веб-разработчиков [devmn.org](https://dvmn.org/modules/).
