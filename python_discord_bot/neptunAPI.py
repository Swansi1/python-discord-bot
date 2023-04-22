"Neptun api kommunikáció"
import datetime
import requests
from weatherAPI import WeatherApi
from dataStruct import User

class Api():
    """"Kommunikáció az API-val"""
    def __init__(self,api_url,neptun_api,weather_api, weather_status_codes) -> None:
        self._neptun_api = neptun_api
        self._api_url = api_url
        self._get_url = self._api_url + "getUsers.php"
        self._reg_url = self._api_url + "registerUser.php"
        self.weather = WeatherApi(weather_api, weather_status_codes)

    def get_users(self) -> list[User]:
        "Vissza adja az összes Users az APIból return List[User_Dict]"
        full_url = self._get_url
        req = requests.get(url = full_url, timeout=5)
        data = req.json()
        users = []
        for user in data:
            users.append(User(user))
        return users

    def get_user(self, dcid) -> User:
        "Vissza adja a megadott Usert"
        full_url = self._get_url
        params = {"dcid": str(dcid)}
        req = requests.get(url = full_url,params=params, timeout=5)
        data = req.json()
        return User(data)

    def register_user(self, username, passwd, eloadas,dcid) -> list[dict]:
        "User mentése az adatbázisba"
        full_url = self._reg_url
        data = {"username": username, "dcid": dcid, "password":passwd, "eloadasShow": eloadas}
        req = requests.post(url = full_url,data=data, timeout=5)
        data = req.json() # vissza adott jsont bele kell appendolni a _users-be
        return data

    def remove_user(self,dcid) -> bool:
        "User törlése az adatbázisból"
        full_url = self._reg_url
        data = {"interaction": "remove", "dcid": str(dcid)}
        req = requests.post(url = full_url,data=data, timeout=5)
        print(req)
        return req.text

    def get_neptun_calendar(self, user:User) -> dict:
        "Lekérdezi az usernek az órarendjét 8 napot kér le"
        try:
            return self._neptun_api_req(user.username,user.password,user.eloadas_show, 8)
        except:
            return {"ErrorMessage":"Hiba az adatok lekérése közben"}

    @staticmethod
    def get_terem_location(terem_kod) -> str:
        "Vissza adja a terem google maps url linkjét ha van"
        url = "http://service.neptun.u-szeged.hu/terem/teremkereso.aspx"
        payload={'search': terem_kod.split(" -")[0]}
        response = requests.request("POST", url, data=payload)
        rt = response.text
        print(rt)
        try:
            google_maps_pattern = rt.split("https://www.google.com/maps/search/")[1].split('"')[0]
        except IndexError:
            google_maps_pattern = "404"
        return "https://www.google.com/maps/search/" + google_maps_pattern

        

    def get_neptun_reg_teszt(self,username,password):
        "Felhasználónév / jelszó ellenőrző hogy jó adatokat adott-e meg"
        req = self._neptun_api_req(username,password,0,1)
        if req["ErrorMessage"] is None:
            return {"error":False}
        return {"error":True,"msg": req["ErrorMessage"]}

    def _neptun_api_req(self, username,password,eloadas,days:int) -> dict:
        current = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        end = current + datetime.timedelta(days=days)
        time_start = int(current.timestamp()) * 1000
        time_end = int(end.timestamp()) * 1000

        payload={'username': username, 'password': password, 'timestamp_start': time_start, 'timestamp_end':time_end}
        req = requests.post(self._neptun_api, data=payload, timeout=5)
        data = req.json() # ez a szar API valamiért vissza adja a jelszót is...
        eloadas = {"eloadasShow": eloadas}
        data.update(eloadas) # adja hozzá hogy bejáre az EA-ra
        return data
