import requests


AREAS = ['SVO', 'London', 'Cherepovets']


def get_weather(area_name):
    params = {'lang': 'ru', 'm': '', 'M': '', 'n': '', 'T': '', 'q': ''}
    url_template = 'http://wttr.in/{}'
    response = requests.get(url_template.format(area_name), params=params)
    response.raise_for_status()
    return response.text


def main():
    for area in AREAS:
        weather_forecast = get_weather(area)
        print(weather_forecast)


if __name__ == '__main__':
    main()
