from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class RideData:
    # данные письма
    mail_to: str
    mail_from: str
    subject: str
    # данные поездки
    ride_dt: datetime
    ride_week_day: str
    ride_cost: float
