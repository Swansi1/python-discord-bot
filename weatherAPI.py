import requests

class WeatherApi():
    "Időjárás API"
    def __init__(self) -> None:
        self._status_codes = [{'status': 1000, 'text': 'Napos idő'}, {'status': 1003, 'text': 'Részben felhős'}, {'status': 1006, 'text': 'Felhős'}, {'status': 1009, 'text': 'Borús'}, {'status': 1030, 'text': 'Gyenge köd'}, {'status': 1063, 'text': 'A közelben eső'}, {'status': 1066, 'text': 'A közelben foltokban havazás'}, {'status': 1069, 'text': 'A közelben foltokban dara'}, {'status': 1072, 'text': 'A közelben foltokban szemerkélő fagyos eső'}, {'status': 1087, 'text': 'A közelben hirtelen vihar'}, {'status': 1114, 'text': 'Hófúvász'}, {'status': 1117, 'text': 'Hóvihar'}, {'status': 1135, 'text': 'Köd'}, {'status': 1147, 'text': 'Jeges köd'}, {'status': 1150, 'text': 'Foltokban enyhe szemerkélő eső'}, {'status': 1153, 'text': 'Enyhe szemerkélő eső'}, {'status': 1168, 'text': 'Fagyos szemerkélő eső'}, {'status': 1171, 'text': 'Heves szemerkélő fagyos eső'}, {'status': 1180, 'text': 'Foltokban enyhe eső'}, {'status': 1183, 'text': 'Enyhe eső'}, {'status': 1186, 'text': 'Időnként mérsékelt eső'}, {'status': 1189, 'text': 'Mérsékelt eső'}, {'status': 1192, 'text': 'Időnként heves eső'}, {'status': 1195, 'text': 'Heves eső'}, {'status': 1198, 'text': 'Enyhe fagyos eső'}, {'status': 1201, 'text': 'Mérsékelt, vagy heves fagyos eső'}, {'status': 1204, 'text': 'Enyhe ólmos eső'}, {'status': 1207, 'text': 'Mérsékelt, vagy heves ólmos eső'}, {'status': 1210, 'text': 'Foltokban enyhe havazás'}, {'status': 1213, 'text': 'Enyhe havazás'}, {'status': 1216, 'text': 'Foltokban mérsékelt havaás'}, {'status': 1219, 'text': 'Mérsékelt havazás'}, {'status': 1222, 'text': 'Foltokban heves havazás'}, {'status': 1225, 'text': 'Heves havazás'}, {'status': 1237, 'text': 'Apró szemű jégeső'}, {'status': 1240, 'text': 'Enyhe eső, zápor'}, {'status': 1243, 'text': 'Mérsékelt, vagy heves felhőszakadás'}, {'status': 1246, 'text': 'Viharos felhőszakadás'}, {'status': 1249, 'text': 'Enyhe ólmos záporeső'}, {'status': 1252, 'text': 'Mérsékelt, vagy heves ólmos záporeső'}, {'status': 1255, 'text': 'Enyhe hózápor'}, {'status': 1258, 'text': 'Mérsékelt, vagy heves hózápor'}, {'status': 1261, 'text': 'Enyhe apró szemű jégeső'}, {'status': 1264, 'text': 'Mérsékelt, vagy heves apró szemű jégeső'}, {'status': 1273, 'text': 'Foltokban enyhe eső mennydörgéssel, villámlással'}, {'status': 1276, 'text': 'A területen foltokban enyhe eső mennydörgéssel, villámlással'}, {'status': 1279, 'text': 'A területen foltokban enyhe havazás mennydörgéssel, villámlással'}, {'status': 1282, 'text': 'Mérsékelt, vagy heves hózápor mennydörgéssel, villámlással'}]
        self._url = "http://api.weatherapi.com/v1/current.json?key=0704db3dc77744e9b38171403231004&q=Szeged&aqi=no"
        self.currentWeather = {}

    def get_current_weather(self):
        "lekéri a jelenlegi időjárást"
        if len(self.currentWeather) == 0:
            self.update_weather()
        return self.currentWeather

    def get_current_weather_string(self) -> str:
        "jelenlegi időjárás str lekérése"
        idojaras = self.get_current_weather()
        return "Időjárás("+ idojaras["name"] +"): Hőmérséklet: " + str(idojaras["temp"]) +"C \n" + idojaras["condition"] + "\nUtolsó frissítés: " + idojaras["last_update"]

    def update_weather(self):
        "jelenlegi időjárás frissítése" 
        # TODO majd a taskba frissítse pl 10 percenként
        req = requests.get(self._url)
        data = req.json()
        condition_hun = self._status_to_text(data["current"]["condition"]["code"])
        dict_return = {"name": data["location"]["name"], "condition": condition_hun, "temp": data["current"]["temp_c"], "last_update": data["current"]["last_updated"]}
        self.currentWeather = dict_return
        return dict_return

    def _status_to_text(self, status_code):
        "Status codebeból magyar text mert alapból angol."
        text = "-"
        for status in self._status_codes:
            if status["status"] == status_code:
                text = status["text"]
                return text
        return text
