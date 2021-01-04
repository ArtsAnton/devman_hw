# Скрип для генерации коротких ссылок и подсчета количества переходов

Скрипт [link.py]() позволяет генеририровать короткую ссылку для вашего ресурса или определяет кличество переходов по сгенерированной ссылки в зависимости от входных данных.

Для работы понадобится зарегистрироваться на [bitly.com](https://bitly.com/) и получить Api token.

Полезные ссылки:
* [Python 3.6.9;](https://www.python.org/downloads/)
* [Библиотека requests 2.25.0;](https://requests.readthedocs.io/en/master/)
* [Библиотека python-dotenv 0.15.0;](https://pypi.org/project/python-dotenv/)
* [Документация bitly.com.](https://dev.bitly.com/)

Установка окружения:
```bash
pip3 install -r requirements.txt
```

Запуск и пример работы кода:
```python3
python3 link.py
Введите ссылку: https://www.google.com/
Битлинк: https://bit.ly/2XjsDfT
```