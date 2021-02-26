import requests
import sys


def convert(temp_kelv: float) -> float:
    if '-f' in params or '--fahrenheit' in params:
        return round((temp_kelv - 273 + 32) * 9 / 5, 1)
    elif '-k' in params or '--kelvin' in params:
        return temp_kelv
    else:
        return round(temp_kelv - 273, 1)


POSSIBLE_PARAMS = {'-a', '--all', '-c', '--cords', '--help', '-f', '--fahrenheit', '-k', '--kelvin'}
MAX_ARGS = 1

params = set()
args = []

for e in sys.argv[1:]:
    if e[0] == '-':
        params.add(e)
    else:
        args.append(e)

if '--help' in params:
    print('''Использование: docker run --rm WeatherStealer [ПАРАМЕТР] [ГОРОД(СТРАНА)]
    Отображает погоду в городе(стране)

        -a, --all           Выводит полную информацию о погоде в системном формате
        -c, --cords         Выводит координаты города(страны)
        -f, --fahrenheit    Выводит температуру в градусах фаренгейта
        -k, --kelvin        Выводит температуру в градусах кельвина

        Коды выхода:
     0  всё отлично,
     1  небольшие проблемы (например, лишние параметры),
     2  серьёзная проблема (например, недоступен аргумент командной строки).''')
    exit(0)

if len(args) == 0:
    print('Пропущен город(страна)')
    print('По команде «--help» можно получить дополнительную информацию.')
    exit(2)

if len(args) > MAX_ARGS:
    print('Лишние аргументы командной строки')
    print('По команде «--help» можно получить дополнительную информацию.')
    exit(2)

exit_code = 0
for e in params:
    if e not in POSSIBLE_PARAMS:
        exit_code = 1
        print(f'Предупреждение: {e} - недопустимый параметр')

if ('-f' in params or '--fahrenheit' in params) and ('-k' in params or '--kelvin' in params):
    exit_code = 1
    print('''Предупреждение: параметры --fahrenheit и --kelvin несовместимы
будет использован параметр --fahrenheit''')

res = requests.get(
    f'http://api.openweathermap.org/data/2.5/weather?q={args[0]}&appid=a9c6ae1633a173476b1b5cb16d08744b').json()

if res['cod'] == '404':
    print(f'Город(страна) {args[0]} не найден')
    exit(2)
else:
    print(f"Город(страна): {res['name']}")
    if '-a' in params or '--all' in params:
        print(res)
    else:
        if '-c' in params or '--cords' in params:
            print(f"Долгота: {res['coord']['lon']}\u00B0")
            print(f"Широта: {res['coord']['lat']}\u00B0")

        print(f"Погода: {res['weather'][0]['description']}")

        tmp_sign = ''
        if '-f' in params or '--fahrenheit' in params:
            tmp_sign = '\u00B0F'
        elif '-k' in params or '--kelvin' in params:
            tmp_sign = 'K'
        else:
            tmp_sign = '\u00B0C'

        print(f"Температура воздуха: {convert(res['main']['temp'])} {tmp_sign}")
        print(f"Ощущаемая температура: {convert(res['main']['feels_like'])} {tmp_sign}")
        print(f"Влажность воздуха: {res['main']['humidity']}%")
        print(f"Давление: {round(res['main']['pressure'] / 1000 * 760)} мм рт. ст.")

exit(exit_code)
