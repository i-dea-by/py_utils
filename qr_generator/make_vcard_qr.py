from typing import NamedTuple


class vCard(NamedTuple):
    name: str
    displayname: str
    email: str | None = None
    phone: str | None = None
    fax: str | None = None
    videophone: str | None = None
    memo: str | None = None
    nickname: str | None = None
    birthday: str | None = None
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
    rev: str | None = None
    title: str | None = None
    photo_uri: str | None = None
    cellphone: str | None = None
    homephone: str | None = None
    workphone: str | None = None

    def __repr__(self):
        return f"<vCard {self.name}>"

