"""Órarend műveletek kezelése"""
import datetime
from .dataStruct import Lesson, LessonType

class CalendarLesson():
    "Órarend kezelése"
    def __init__(self,calendar,eloadas=0) -> None:
        self._orak:list[Lesson] = [] # Lesson Obj-k vannak benne

        self._is_ea = int(eloadas) # 0 / 1 | 0 = Nem jár be az előadásra és úgy adja vissza
        self._current_time = datetime.datetime.now()
        self._today = datetime.date.today()
        self._init_lesson(calendar)

    def _init_lesson(self, osszes_ora:dict):
        for ora in osszes_ora:
            new_ora = Lesson(ora)
            self._orak.append(new_ora)

    def _update_time(self) -> None:
        "up-to-date legyen a dátum"
        self._current_time = datetime.datetime.now() # + datetime.timedelta(days=_TESZT)
        self._today = datetime.date.today() #+ datetime.timedelta(days=_TESZT)

    def get_exam(self) -> list[Lesson]:
        "Elkövetkezendő vizsgák lekérése"
        kovi_vizsga = [] # dictet insertelünk bele azazh egy órát
        for i in range(0,8):  # 8 napot kér le az api
            # hozzá ad mindig 1 napot mert lehet nem ma van a kövi óra
            for ora in self._get_lesson_from_date(self._today + datetime.timedelta(days=i), LessonType.VIZSGA):
                ora_kezdes = ora.get_start_datetime()
                if  ora_kezdes > self._current_time: # dátum szerint van rendezve
                    kovi_vizsga.append(ora)
                    return kovi_vizsga
        return kovi_vizsga

    def get_next_lesson(self) -> list[Lesson]:
        '''Következő óra visszaadása dict[Lesson]'''
        self._update_time()

        # list-be adja vissza a dictet... ne csak 1 dictet
        kovi_ora = [] # dictet insertelünk bele azazh egy órát
        for i in range(0,8):  # 8 napot kér le az api
            # hozzá ad mindig 1 napot mert lehet nem ma van a kövi óra
            for ora in self._get_lesson_from_date(self._today + datetime.timedelta(days=i)):
                ora_kezdes = ora.get_start_datetime()
                if  ora_kezdes > self._current_time: # dátum szerint van rendezve
                    kovi_ora.append(ora)
                    return kovi_ora
        return kovi_ora

    def get_today_lesson(self) -> list[Lesson]:
        "Összes mai óra lekérése"
        self._update_time()
        return self._get_lesson_from_date(self._today)

    def get_tomorrow_lesson(self) -> list[Lesson]:
        "Összes holnapi óra lekérése"
        self._update_time()
        tommorrow = self._today + datetime.timedelta(days=1)
        return self._get_lesson_from_date(tommorrow)

    def _get_lesson_from_date(self,date: datetime.date, search=LessonType.IDK) -> list[Lesson]:
        "Órák visszaadása egy adott napra, csak egy helper def"
        today_lessons = []
        current_date = date
        for lesson in self._orak:
            if search != LessonType.IDK: # ha van szűrés
                if lesson.type != search:
                    continue
            if self._is_ea == 0: # EA szűrése ha nem jár be előadásra a jobbágy
                if lesson.is_ea:
                    continue
            if current_date == lesson.get_start_date():
                today_lessons.append(lesson)
        return today_lessons
