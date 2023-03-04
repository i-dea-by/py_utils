from dataclasses import dataclass
from datetime import date
from typing import NamedTuple

@dataclass
class DCvCard:
    """
        https://ru.wikipedia.org/wiki/VCard
    """
    displayname: str  # FN - Полное имя в виде единой строки без разделителей
    name: str | None = None  # N - фамилия; имя; отчество (дополнительные имена); префиксы; суффиксы
    nickname: str | None = None
    email: str | None = None
    phone: str | None = None
    fax: str | None = None
    videophone: str | None = None
    memo: str | None = None
    birthday: str | date | None = None
    url: str | None = None
    # ADR (pobox, street, city, region, zipcode, country)
    pobox: str | None = None  # P.O. box (address information).
    street: str | None = None  # Street address.
    city: str | None = None  # City (address information).
    region: str | None = None  # Region (address information).
    zipcode: str | None = None  # Zip code (address information).
    country: str | None = None  # Country (address information).
    org: str | None = None
    lat: str | None = None
    lng: str | None = None
    source: str | None = None
    rev: str | date | None = None
    title: str | None = None
    photo_uri: str | None = None
    cellphone: str | None = None
    homephone: str | None = None
    workphone: str | None = None

    def __post_init__(self):
        if self.name is None:
            self.name = self.displayname.replace(' ', ';')

    def to_dict(self):
        _dict = {key: value for key, value in self.__dict__.items() if value is not None}
        return _dict

    def __repr__(self):
        return f"<vCard {self.displayname}>"


class NTvCard(NamedTuple):
    """
        https://ru.wikipedia.org/wiki/VCard
    """
    name: str  # фамилия; имя; отчество (дополнительные имена); префиксы; суффиксы
    displayname: str  # Полное имя в виде единой строки
    nickname: str | None = None
    email: str | None = None
    phone: str | None = None
    fax: str | None = None
    videophone: str | None = None
    memo: str | None = None
    birthday: str | date | None = None
    url: str | None = None
    pobox: str | None = None
    street: str | None = None
    city: str | None = None
    region: str | None = None
    zipcode: str | None = None
    country: str | None = None
    org: str | None = None
    lat: str | None = None
    lng: str | None = None
    source: str | None = None
    rev: str | date | None = None
    title: str | None = None
    photo_uri: str | None = None
    cellphone: str | None = None
    homephone: str | None = None
    workphone: str | None = None

    def __repr__(self):
        return f"<vCard {self.displayname}>"