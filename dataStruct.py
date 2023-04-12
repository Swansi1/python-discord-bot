import datetime

class User():
    "Egy adott user felhasználónak az adatainak tárolására szolgáló osztály"
            
    def __init__(self, userDict) -> None:
        "Dict alapján init user"
        self._dcid = userDict["dcid"]
        self._username = userDict["username"]
        self._passwd = userDict["password"]
        self._eloadasShow = userDict["eloadasShow"]
    
    @property
    def dcid(self):
        return self._dcid
    
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._passwd
    
    @property
    def eloadasShow(self):
        return self._eloadasShow

class Lesson():
    def __init__(self,ora: dict) -> None:
        # ilet kap: {'start': '1681308000000', 'end': '1681311600000', 'title': 'Formális nyelvek gyakorlat (IBK403G)', 'location': 'IR-219-3 - Irinyi 219 tanterem(IR-219-3)'}
        ora = self._lessonFormater(ora)
        self._start = int(ora["start"]) / 1000 #! datetime.datetime.fromtimestamp miatt, hogy ott ne kelljen osztogatni
        self._end = int(ora["end"]) / 1000 
        self._title = ora["title"]
        self._location = ora["location"]
        self._IsEA = ora["isEA"] # adott óra előadás-e
        
        
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
    def isEA(self) -> bool:
        "Vissza adja, hogy az adott óra Előadás-e, Igaz ha előadás"
        return self._IsEA
    
    def get_start_date(self) -> datetime.date:
        "Vissza adja az óra kezdését datetime.date formátumban"
        return datetime.date.fromtimestamp(self._start) 
    
    def get_start_datetime(self) -> datetime.datetime:
        "Vissza adja az óra kezdését datetime.date formátumban"
        return datetime.datetime.utcfromtimestamp(self._start) #TODO nem biztos de itt fromtimestamp volt, de a másik kell szerintem mert a noe jól kéri le az időt..
    
    def get_end_datetime(self) -> datetime.datetime:
        "Vissza adja az óra befejezésének datetime.datetime-ját"
        return datetime.datetime.utcfromtimestamp(self._end)
    
    def get_mettol_meddig(self) -> str:
        "Vissza adja hogy mikor, mettől meddig tart az óra pl: 2023.04.12 14:00 - 16:00"
        return self.get_start_datetime().strftime("%Y-%m-%d %H:%M") + " - " + self.get_end_datetime().strftime("%H:%M")
    
    def _lessonFormater(self,lesson):
        "Sok hülyeség kiszedése, timestampok fixálása, óra neve rövidítése"
        # print(lesson)
        # title syntax
        # syntax = '[Órarend Szünnap]    -Tavaszi tanítási szünet (Spring school break)'
        # syntax = "[Óra] Hardware és software rendszerek verifikációja (IBK615G)  - IB615G-1   Minden hét (Gombás Éva Dr.) (IR-223-3 - Irinyi 223 PC-terem(IR-223-3))"
        newLesson = {}
        startTimeStamp = lesson["start"].split("(")[1].split(")")[0]
        # startDateTime = datetime.datetime.utcfromtimestamp(int(startTimeStamp)/1000.0)

        endTimeStamp =lesson["end"].split("(")[1].split(")")[0]
        # endDateTime = datetime.datetime.utcfromtimestamp(int(endTimeStamp)/1000.0)
        newTitle = lesson["title"]
        isEA = False
        try:
            if 'e)' in newTitle or 'E)' in newTitle:
                isEA = True
                
            if '[Óra]' in newTitle: # Todo több iffel bővíteni (nem tudom hogy írja a vizsgákat) VIZSGA: [Vizsga]
                newTitle = newTitle.split("]")[1].split("-")[0].strip()
        except Exception as e:
            pass
        newLesson["start"] = startTimeStamp
        newLesson["end"] = endTimeStamp
        newLesson["title"] = newTitle
        newLesson["location"] = lesson["location"]
        newLesson["isEA"] = isEA
        return newLesson