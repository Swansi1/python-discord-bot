import datetime
from dataStruct import Lesson

class CalendarLesson():
    "Órarend kezelése"
    def __init__(self,calendar,eloadas=0) -> None:
        self._orak:list[Lesson] = [] # Lesson Obj-k vannak benne
        
        self._isEloadas = int(eloadas) # TODO must 0 / 1 | 0 = Nem jár be az előadásra és úgy adja vissza
        self._currentTime = datetime.datetime.now()
        self._today = datetime.date.today()
        self._init_lesson(calendar)
    
    
    def _init_lesson(self, osszesOra:dict):
        for ora in osszesOra:
            ujOra = Lesson(ora)
            self._orak.append(ujOra)
    
    def _updateTime(self) -> None: # nem kell paramétert megadni a teszt csak hogy hány nappal tolja el
        "up-to-date legyen a dátum"
        self._currentTime = datetime.datetime.now() # + datetime.timedelta(days=_TESZT) #! CSAK TESZT MIATT!!!!
        self._today = datetime.date.today() #+ datetime.timedelta(days=_TESZT)
        
    def get_next_lesson(self) -> list[Lesson]:
        '''Következő óra visszaadása dict[Lesson]'''
        self._updateTime()

        # list-be adja vissza a dictet... ne csak 1 dictet
        koviOra = [] # dictet insertelünk bele azazh egy órát
        for i in range(0,8):  # azért 8ig mert 8 napot kér le az API Igazából ide 9 kéne mert a last nicns benne
            for ora in self._get_lesson_from_date(self._today + datetime.timedelta(days=i)): # hozzá ad mindig 1 napot mert lehet nem ma van a kövi óra
                oraKezdes = ora.get_start_datetime()
                print("current",self._currentTime)
                print("orakezdes", oraKezdes)
                if  oraKezdes > self._currentTime: # dátum szerint vannak a list-ben szóval az első találat a kapó
                    # kezdés > mint a mostani 
                    koviOra.append(ora)
                    return koviOra 
        return koviOra 
    
    def get_today_lesson(self) -> list[Lesson]:
        "Összes mai óra lekérése"
        self._updateTime()
        return self._get_lesson_from_date(self._today)
    
    def get_tomorrow_lesson(self) -> list[Lesson]:
        "Összes holnapi óra lekérése"
        self._updateTime()
        tommorrow = self._today + datetime.timedelta(days=1)
        return self._get_lesson_from_date(tommorrow)
    
    def _get_lesson_from_date(self,date: datetime.date) -> list[Lesson]:
        "Órák visszaadása egy adott napra, csak egy helper def"
        todayLessons = []
        currentDate = date
        for lesson in self._orak:
            try:
                if self._isEloadas == 0: # EA szűrése ha nem jár be előadásra a jobbágy
                    if lesson.isEA: 
                        continue
            except:
                pass
            if currentDate == lesson.get_start_date():
                todayLessons.append(lesson)
        return todayLessons
        