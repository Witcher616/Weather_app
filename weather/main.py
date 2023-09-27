import requests
import json
from .utils import convert_seconds_to_date
import config
from Db import queries as sql


def get_weather():
    data = []
    username = input("Enter username: ")
    is_exists, user_id = sql.check_user_exists('weather.db', username)

    if not is_exists:
        sql.add_user('weather.db', username)
        get_weather()
    else:
        while True:
            city = input('Напишите сввой город: ')

            if city == 'stop':
                break

            if city == 'save':
                with open('weather.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                continue
            elif city == 'show':
                all_weather = sql.get_user_weather('weather.db', user_id)

                if not all_weather:
                    print('Empty')
                    continue
                for item in all_weather:
                    response = requests.get(config.url, params=config.parameters).json()
                    timezone = response['timezone']
                    name, _, sunrise, sunset, dt, description, speed, temp = item[1:-1]
                    print(f"""
================================================
В городе {name} сейчас {description}
Температура: {temp}
Скорость ветра: {speed}
Восход солнца: {convert_seconds_to_date(sunrise, timezone)}
Закат солнца: {convert_seconds_to_date(sunset, timezone)}
Время отправки запроса: {convert_seconds_to_date(dt, timezone)}
================================================
""")
                continue
            elif city == 'clear':
                sql.clear_user_weather('weather.db', user_id)
                print('История очищена')
                continue

            config.parameters['q'] = city

            response = requests.get(config.url, params=config.parameters).json()

            name = response['name']
            sunrise = response['sys']['sunrise']
            sunset = response['sys']['sunset']
            dt = response['dt']
            description = response['weather'][0]['description']
            timezone = response['timezone']
            speed = response['wind']['speed']
            temp = response['main']['temp']

            sql.add_weather("weather.db",
                            name=name,
                            tz=timezone,
                            sunrise=sunrise,
                            sunset=sunset,
                            dt=dt,
                            description=description,
                            speed=speed,
                            temp=temp,
                            user_id=user_id
                            )

            data.append(
                dict(
                    zip(
                        ['name', 'sunrise', 'sunset', 'description', 'speed'],
                        [name, convert_seconds_to_date(sunrise, timezone), convert_seconds_to_date(sunset, timezone), description, speed]
                    )
                )
            )

            print(f"""
================================================
В городе {name} сейчас {description}
Температура: {temp}
Скорость ветра: {speed}
Восход солнца: {convert_seconds_to_date(sunrise,timezone)}
Закат солнца: {convert_seconds_to_date(sunset, timezone)}
Время отправки запроса: {convert_seconds_to_date(dt, timezone)}
================================================
""")



