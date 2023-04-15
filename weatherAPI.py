"""Időjárás API-val való kommunikáció"""
import requests

class WeatherApi():
    "Időjárás API"

    def __init__(self, api_url, status_codes) -> None:
        self._status_codes = status_codes
        self._url = api_url
        self.current_weather = {}

    def get_current_weather(self):
        "lekéri a jelenlegi időjárást"
        if len(self.current_weather) == 0:
            self.update_weather()
        return self.current_weather

    def get_current_weather_string(self) -> str:
        "jelenlegi időjárás str lekérése"
        idojaras = self.get_current_weather()
        idojaras_str = "Időjárás(" + idojaras["name"] + "): "
        homerseklet_str = "Hőmérséklet: " + str(idojaras["temp"]) + "C\n" + idojaras["condition"]
        frissites_str = "\nUtolsó frissítés: " + idojaras["last_update"]
        return idojaras_str + homerseklet_str + frissites_str

    def update_weather(self): # TODO request try
        "jelenlegi időjárás frissítése"
        req = requests.get(self._url, timeout=5)
        data = req.json()
        condition_hun = self._status_to_text(
            data["current"]["condition"]["code"])
        dict_return = {"name": data["location"]["name"], "condition": condition_hun,
                       "temp": data["current"]["temp_c"], "last_update": data["current"]["last_updated"]}
        self.current_weather = dict_return
        return dict_return

    def _status_to_text(self, status_code):
        "Status codebeból magyar text mert alapból angol."
        text = "-"
        for status in self._status_codes:
            if status["status"] == status_code:
                text = status["text"]
                return text
        return text
