# Скрипт для генерации коротких ссылок и подсчета количества переходов

Скрипт [link.py](https://github.com/ArtsAnton/devman_hw/blob/main/api/les2/link.py) позволяет сгенерировать короткую ссылку для вашего ресурса или определяет количество переходов по сгенерированной ссылке в зависимости от входных данных.

Для работы понадобится зарегистрироваться на [bitly.com](https://bitly.com/) и получить Api token.

### Полезные ссылки:
* [Python 3.6.9;](https://www.python.org/downloads/)
* [Библиотека requests 2.25.0;](https://requests.readthedocs.io/en/master/)
* [Библиотека python-dotenv 0.15.0;](https://pypi.org/project/python-dotenv/)
* [Документация bitly.com.](https://dev.bitly.com/)

### Установка окружения:
```bash
pip3 install -r requirements.txt
```

### Запуск и пример работы кода:
```python3
python3 link.py https://www.google.com/
Битлинк: https://bit.ly/2XjsDfT
```

### Цель проекта

Код написан в образовательных целях в рамках выполнения уроков № 2 и № 3 онлайн-курса для веб-разработчиков [devmn.org](https://dvmn.org/modules/web-api/).