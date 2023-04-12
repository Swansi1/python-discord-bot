import requests, datetime
from weatherAPI import WeatherApi
from dataStruct import User

class Api():
    """"Kommunikáció az API-val"""
    global users
    def __init__(self,api_url) -> None:
        self._api_url = api_url
        self._get_url = self._api_url + "getUsers.php"
        self._reg_url = self._api_url + "registerUser.php"
        self.weather = WeatherApi()
    
    def get_users(self) -> list[User]:
        "Vissza adja az összes Users az APIból return List[User_Dict]"
        full_url = self._get_url
        req = requests.get(url = full_url)
        data = req.json()
        users = []
        for u in data: 
            users.append(User(u))
        return users
    
    def get_user(self, dcid) -> User:
        "Vissza adja a megadott Usert -> dcid-t vár és abból kéri ki az id-t ami alapján azonosítja az userst"
        full_url = self._get_url
        params = {"dcid": str(dcid)}
        req = requests.get(url = full_url,params=params)
        data = req.json()
        return User(data)
    
    def register_user(self, username, passwd, eloadas,dcid) -> list[dict]:
        "User mentése az adatbázisba"
        full_url = self._reg_url
        data = {"username": username, "dcid": dcid, "password":passwd, "eloadasShow": eloadas}
        req = requests.post(url = full_url,data=data)
        data = req.json() # vissza adott jsont bele kell appendolni a _users-be
        return data

    def get_neptun_calendar(self, user:User) -> dict:
        "Lekérdezi az usernek az órarendjét 8 napot kér le, cuser = DCID"
        current = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        end = current + datetime.timedelta(days=8)
        time_start = int(current.timestamp()) * 1000
        time_end = int(end.timestamp()) * 1000

        url = "http://swansi.hu:8000/neptun/naptar"
        payload={'username': user.username, 'password': user.password, 'timestamp_start': time_start, 'timestamp_end':time_end}
        req = requests.post(url, data=payload)
        data = req.json() # ez a szar API valamiért vissza adja a jelszót is...
        eloadas = {"eloadasShow": user.eloadasShow}
        data.update(eloadas) # adja hozzá hogy bejáre az EA-ra 
        return data
   