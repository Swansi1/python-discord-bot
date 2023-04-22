import unittest
from  python_discord_bot.weatherAPI import WeatherApi

class weatherAPI_test(unittest.TestCase):
    def setUp(self) -> None:
        self.api = WeatherApi("http://api.weatherapi.com/v1/current.json?key=0704db3dc77744e9b38171403231004&q=Szeged&aqi=no",[{"status":1000, "text" : "valami"}])
        
    def test_init(self):
        self.assertEqual(self._status_codes, [{"status":1000, "text" : "valami"}], "Nem megfelelő status_code")
        self.assertEqual(self._url,"http://api.weatherapi.com/v1/current.json?key=0704db3dc77744e9b38171403231004&q=Szeged&aqi=no", "nem jó url" )

if __name__ == '__main__':
    unittest.main()
