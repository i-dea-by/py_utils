import dataclasses
import json
from datetime import datetime
from pathlib import Path
from typing import TypeVar, Any

from uber_cost_by_year.ride_data import RideData

PathLike = TypeVar("PathLike", str, Path)


# --------------- JSON serialize/deserialilze ---------------

class _JSONencoder(json.JSONEncoder):
    """ Класс для сериализации json """

    def default(self, obj):
        # если попался dataclass
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        # если попался datetime
        if isinstance(obj, datetime):
            return obj.replace(tzinfo=None).isoformat()
        if isinstance(obj, Path):
            return obj.name
        return super().default(obj)


class _JSONdecoder(json.JSONDecoder):
    """ Класс для десериализации json """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def try_datetime(value):
        try:
            result = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            return False
        return result

    @staticmethod
    def try_ride_data(value: dict):
        # если не None значит это данные поездки
        if value.get('ride_dt'):
            return RideData(
                mail_to=value['mail_to'],
                mail_from=value['mail_from'],
                subject=value['subject'],
                ride_dt=_JSONdecoder.try_datetime(value['ride_dt']),
                ride_week_day=value['ride_week_day'],
                ride_cost=value['ride_cost'],
            )
        return False

    @staticmethod
    def object_hook(obj):
        """ Перебор объектов на предмет того, что это за структура """

        if result := _JSONdecoder.try_ride_data(obj):
            return result

        result = {}
        for key, value in obj.items():
            if _value := _JSONdecoder.try_datetime(value):
                result[key] = _value
            else:
                result[key] = value
        return result


def save_as_jsonfile(obj: Any, filename: PathLike):
    """ Сохраняет объект в json-файл """
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(to_json_str(obj))


def load_jsonfile(filename: PathLike) -> list | dict:
    """ Загружает json-файл в объект """
    with open(filename, 'r', encoding='utf-8') as f:
        return from_json_str(f.read())


def to_json_str(obj: Any, indent: int = 4) -> str:
    """ Возвращает json-строку из переданного объекта на основе json.dumps """
    return json.dumps(obj, cls=_JSONencoder, ensure_ascii=False, indent=indent)


def from_json_str(_str: str) -> list | dict:
    """ Декодирует json-строку в объект, на основе json.loads """
    return json.loads(_str, cls=_JSONdecoder)
