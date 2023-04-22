import unittest
from unittest.mock import mock_open, patch
from config import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.valid_config = {
            "NEPTUN_API_URL": "https://neptun-api.com",
            "WEATHER_API_URL": "https://weather-api.com",
            "USERS_API_URL": "https://users-api.com",
            "BOT_TOKEN": "1234567890",
            "WEATHER_STATUS_CODES": [200, 201, 202]
        }
        self.invalid_config = {}

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_config_file_not_found(self, mock_file):
        config = Config()
        self.assertTrue(config.is_error)

    @patch("builtins.open", new_callable=mock_open, read_data='{"invalid_key": "value"}')
    def test_invalid_config_file(self, mock_file):
        config = Config()
        self.assertEqual(config.neptun_api, None)

    @patch("builtins.open", new_callable=mock_open, read_data='{"NEPTUN_API_URL": "https://neptun-api.com", "WEATHER_API_URL": "https://weather-api.com", "USERS_API_URL": "https://users-api.com", "BOT_TOKEN": "1234567890", "WEATHER_STATUS_CODES": [200, 201, 202]}')
    def test_valid_config_file(self, mock_file):
        config = Config()
        self.assertEqual(config.neptun_api, "https://neptun-api.com")
        self.assertEqual(config.weather_api, "https://weather-api.com")
        self.assertEqual(config.users_api, "https://users-api.com")
        self.assertEqual(config.bot_token, "1234567890")
        self.assertEqual(config.weather_status_codes, [200, 201, 202])

if __name__ == '__main__':
    unittest.main()