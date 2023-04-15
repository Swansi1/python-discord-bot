import json

class Config():
    "Config file betöltése a config.json fileból"
    def __init__(self) -> None:
        self._config = []
        self.is_error = False
        try:
            with open("config.json", "r", encoding="utf-8") as conf:
                config = json.loads(conf.read())
                self._config = config
        except FileNotFoundError:
            self.is_error = True

    @property
    def neptun_api(self) -> str:
        "neptun api URL "
        return self._config["NEPTUN_API_URL"]

    @property
    def weather_api(self) -> str:
        "Weather api url"
        return self._config["WEATHER_API_URL"]

    @property
    def users_api(self) -> str:
        "Users api url"
        return self._config["USERS_API_URL"]

    @property
    def bot_token(self) -> str:
        "Bot token str"
        return self._config["BOT_TOKEN"]

    @property
    def weather_status_codes(self):
        "Weathet status codes"
        return self._config["WEATHER_STATUS_CODES"]
