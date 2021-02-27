# Урок №4  курса ["API веб-сервисов".](https://dvmn.org/modules/web-api/lesson/space-instagram/#17) 

Настоящий проект позволяет автоматизировать процесс ведения тематического аккаунта в Instagram.


Состав проекта:
1. Файлы для генерации контента - [spacex.py](https://github.com/ArtsAnton/devman_hw/blob/main/api/les_4/spacex.py), [hubble.py](https://github.com/ArtsAnton/devman_hw/blob/main/api/les_4/hubble.py);
2. Файл для загрузки контента в Instagram - [download.py](https://github.com/ArtsAnton/devman_hw/blob/main/api/les_4/download.py).

Полезные ссылки:

* [Библиотека requests](https://requests.readthedocs.io/en/master/user/install/#install);
* [Библиотека python-dotenv](https://pypi.org/project/python-dotenv/);
* [Библиотека Pillow](https://pillow.readthedocs.io/en/stable/);
* [Библиотека instabot](https://pypi.org/project/instabot/);
* [Spacex API](https://docs.spacexdata.com/);
* [Hubble API](https://hubblesite.org/api/documentation).

Начало работы:
1. Зарегистрируйтесь в [Instagram](https://www.instagram.com/);
2. Создайте файл .env для хранения INST_PASSWORD='...', INST_LOGIN='...';
3. Подготовка к работе;

```
pip install virtualenv
source venv/bin/activate
pip install -r requirements.txt 
```
4. Скачиваем фотографии spacex;
```
python3 spacex.py
```
5. Скачиваем фотографии hubble;
```
python3 hubble.py collection_name
```
collection_name - имя коллекции фотографий hubble.
6. Загружаем контент в Instagram;

### Цель проекта

Код написан в образовательных целях в рамках выполнения урока № 4 онлайн-курса для веб-разработчиков [devmn.org](https://dvmn.org/modules/).
