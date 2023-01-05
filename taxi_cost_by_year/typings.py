#################################################
#               Typings and Classes             #
#################################################
import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass(slots=True)
class RideDataUber:
    # данные письма
    mail_to: str
    mail_from: str
    subject: str
    # данные поездки
    ride_dt: datetime
    ride_week_day: str
    ride_cost: float
    ride_distance: float


@dataclass(slots=True)
class RideData:
    ride_from: str
    ride_to: str
    duration: timedelta | None
    ride_dt: datetime | None
    ride_cost: float
    ride_distance: float


class CustomJSONencoder(json.JSONEncoder):
    """ Преобразует объект json-строку
    """

    def default(self, obj):
        # если попался dataclass
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        # если попался datetime
        if isinstance(obj, datetime):
            return obj.replace(tzinfo=None).isoformat()
        if isinstance(obj, timedelta):
            return obj.seconds
        if isinstance(obj, Path):
            return obj.name
        return super().default(obj)


class CustomJSONdecoder(json.JSONDecoder):
    """ Класс для десериализации json """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def as_ride_data(value: dict):
        return RideData(
            ride_from=value['ride_from'],
            ride_to=value['ride_to'],
            duration=timedelta(seconds=value['duration']),
            ride_dt=datetime.fromisoformat(value['ride_dt']),
            ride_cost=value['ride_cost'],
            ride_distance=value['ride_distance']
        )

    @staticmethod
    def object_hook(obj: dict):
        """ Перебор объектов на предмет того, что это за структура """

        # если в словаре есть 'ride_dt' значит пришли данные поездки
        if 'ride_dt' in obj:
            return CustomJSONdecoder.as_ride_data(obj)

        return obj
