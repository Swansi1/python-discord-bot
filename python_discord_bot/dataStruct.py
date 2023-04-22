"""User, Lesson adatszerkezetek"""
import datetime
from enum import Enum

class User():
    "Egy adott user felhasználónak az adatainak tárolására szolgáló osztály"

    def __init__(self, user_dict) -> None:
        self._dcid = user_dict["dcid"]
        self._username = user_dict["username"]
        self._passwd = user_dict["password"]
        self._eloadas_show = user_dict["eloadasShow"]
        self.is_error_reported = False

    @property
    def dcid(self) -> str:
        "Vissza adja a dcid-t"
        return self._dcid

    @property
    def username(self) -> str:
        "Vissza adja az usernamet"
        return self._username

    @property
    def password(self) -> str:
        "Vissza adja a jelszót"
        return self._passwd

    @property
    def eloadas_show(self) -> int:
        "Vissza adja, hogy bejár-e előadásra"
        return self._eloadas_show

class Lesson():
    "óra kezelése"
    def __init__(self, ora: dict) -> None:
        ora = self._lesson_formater(ora)
        # ! datetime.datetime.fromtimestamp miatt, hogy ott ne kelljen osztogatni
        self._start = int(ora["start"]) / 1000
        self._end = int(ora["end"]) / 1000
        self._title = ora["title"]
        self._location = ora["location"]
        self._is_ea = ora["isEA"]  # adott óra előadás-e
        self._type = ora["type"]

    @property
    def start_timestamp(self) -> int:
        "vissza adja az óra kezdését timestamptben epocs-ban NEM milisecben!"
        return self._start

    @property
    def end_timestamp(self) -> int:
        "Vissza adja az óra végét timestamptben epocsban NEM milisecben!"
        return self._end

    @property
    def title(self) -> str:
        "Vissza adja az óra nevét"
        return self._title

    @property
    def location(self) -> str:
        "Vissza adja az óra helyét"
        return self._location

    @property
    def is_ea(self) -> bool:
        "Vissza adja, hogy az adott óra Előadás-e, Igaz ha előadás"
        return self._is_ea

    @property
    def type(self) -> Enum:
        "Enum lesson type"
        return self._type

    def get_start_date(self) -> datetime.date:
        "Vissza adja az óra kezdését datetime.date formátumban"
        return datetime.date.fromtimestamp(self._start)

    def get_start_datetime(self) -> datetime.datetime:
        "Vissza adja az óra kezdését datetime.date formátumban"
        return datetime.datetime.utcfromtimestamp(self._start)

    def get_end_datetime(self) -> datetime.datetime:
        "Vissza adja az óra befejezésének datetime.datetime-ját"
        return datetime.datetime.utcfromtimestamp(self._end)

    def get_mettol_meddig(self) -> str:
        "Vissza adja hogy mikor, mettől meddig tart az óra pl: 2023.04.12 14:00 - 16:00"
        ora_kezdes = self.get_start_datetime().strftime("%Y-%m-%d %H:%M")
        ora_vege = self.get_end_datetime().strftime("%H:%M")
        return ora_kezdes + " - " + ora_vege

    def _lesson_formater(self, lesson):
        "Sok hülyeség kiszedése, timestampok fixálása, óra neve rövidítése"
        # print(lesson)
        # title syntax
        # syntax = '[Órarend Szünnap]    -Tavaszi tanítási szünet (Spring school break)'
        # syntax = "[Óra] Hardware és software rendszerek verifikációja (IBK615G)
        new_lesson = {}
        start_time_stamp = lesson["start"].split("(")[1].split(")")[0]
        # startDateTime = datetime.datetime.utcfromtimestamp(int(start_time_stamp)/1000.0)

        end_time_stamp = lesson["end"].split("(")[1].split(")")[0]
        # endDateTime = datetime.datetime.utcfromtimestamp(int(end_time_stamp)/1000.0)
        new_title = lesson["title"]
        is_ea = False
        types = LessonType.IDK
        try:
            if 'e)' in new_title or 'E)' in new_title:
                is_ea = True
                types = LessonType.EA

            # Todo több iffel bővíteni (nem tudom hogy írja a vizsgákat) VIZSGA: [Vizsga]
            if '[Óra]' in new_title:
                new_title = new_title.split("]")[1].split("-")[0].strip()

            if '[Vizsga]' in new_title:
                types = LessonType.VIZSGA
        except Exception as e:
            print("hiba", str(e))
        new_lesson["start"] = start_time_stamp
        new_lesson["end"] = end_time_stamp
        new_lesson["title"] = new_title
        new_lesson["location"] = lesson["location"]
        new_lesson["isEA"] = is_ea
        new_lesson["type"] = types
        return new_lesson


class LessonType(Enum):
    "Lesson types"
    EA = "Előadás"
    GYAK = "Gykorlat"
    VIZSGA = "Vizsga"
    IDK = "ismeretlen"
