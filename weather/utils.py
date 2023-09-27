from datetime import datetime

def convert_seconds_to_date(seconds: int, timezone: int):
    """Конверируем секунды в удобночитаемый вид, учитывая часовой пояс"""
    return datetime.utcfromtimestamp(seconds + timezone).strftime("%H:%M:%S")