from unittest import IsolatedAsyncioTestCase
import unittest
import weatherFunctions

TEST_GUILD_ID = 1 #Going under assumption that no discord server has guild id of TESTID
WEATHER_API_KEY = "b21b205ea20945d9135435890e29249d"
class WeatherTests(IsolatedAsyncioTestCase):
  def test(self):
    self.assertTrue(True)

  # Testing valid city inputs
  def test_getWeather_validCities(self):
    cities = ["New York", "Amsterdam", "London"]
    unit_sys = "imperial"
    for city in cities:
      expected_response = f"In ***{city}***, it's"
      response = weatherFunctions.getWeather(city, unit_sys, WEATHER_API_KEY)
      self.assertIn(expected_response, response)

  # Testing valid city input (long form of city name)
  def test_getWeather_validCityLong(self):
    city = "Santa Cruz, CA, USA"
    unit_sys = "imperial"
    expected_response = "In ***Santa Cruz***, it's"
    response = weatherFunctions.getWeather(city, unit_sys, WEATHER_API_KEY)
    self.assertIn(expected_response, response)
      

  # Testing invalid city inputs
  def test_getWeather_invalidCities(self):
    cities = ["Fake City", " ", "", None]
    unit_sys = "imperial"
    for city in cities:
      expected_response = "Error retrieving weather data: Invalid city provided\nSet a valid city with =setCity <city>"
      response = weatherFunctions.getWeather(city, unit_sys, WEATHER_API_KEY)
      self.assertEqual(expected_response, response)

  # Testing valid unit inputs
  def test_getWeather_validUnits(self):
    city = "New York"
    unit_sys = "imperial"
    expected_response = f"In ***{city}***, it's"
    response = weatherFunctions.getWeather(city, unit_sys, WEATHER_API_KEY)
    self.assertIn(expected_response, response)
    self.assertIn("°F", response)
    unit_sys = "metric"
    expected_response = f"In ***{city}***, it's"
    response = weatherFunctions.getWeather(city, unit_sys, WEATHER_API_KEY)
    self.assertIn(expected_response, response)
    self.assertIn("°C", response)

  # Testing invalid unit inputs
  def test_getWeather_invalidUnits(self):
    city = "New York"
    unit_systems = ["fake_system", " ", "", None]
    expected_response = "Error retrieving weather data: invalid unit system"
    for unit_sys in unit_systems:
      response = weatherFunctions.getWeather(city, unit_sys, WEATHER_API_KEY)
      self.assertEqual(expected_response, response)

  # Testing valid weather api key
  def test_getWeather_validKey(self):
    city = "New York"
    unit_sys = "imperial"
    expected_response = f"In ***{city}***, it's"
    response = weatherFunctions.getWeather(city, unit_sys, WEATHER_API_KEY)
    self.assertIn(expected_response, response)

  # Testing invalid weather api key
  def test_getWeather_invalidKey(self):
    city = "New York"
    unit_sys = "imperial"
    weather_api_keys = [None, " ", "", "invalid_key"]
    expected_response = "Error retrieving weather data: Invalid or no API key provided"
    for weather_api_key in weather_api_keys:
      response = weatherFunctions.getWeather(city, unit_sys, weather_api_key)
      self.assertEqual(expected_response, response)

  # Testing valid city inputs
  async def test_setCity_validCities(self):
    cities = ["New York", "Amsterdam", "London"]
    for city in cities:
      expected_response = f"Location set to {city}"
      response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
      self.assertEqual(expected_response, response)

  # Testing invalid city inputs
  async def test_setCity_invalidCities(self):
    cities = [" ", "", None]
    for city in cities:
      expected_response = "Error setting city: Invalid city provided\nSet a valid city with =setCity <city>"
      response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
      self.assertEqual(expected_response, response)

  # Testing valid guild_id inputs
  async def test_setCity_validGuildIds(self):
    city = "New York"
    expected_response = f"Location set to {city}"
    response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
    self.assertEqual(expected_response, response)

  # Testing invalid guild_id inputs
  async def test_setCity_invalidGuildIds(self):
    city = "New York"
    bad_guild_ids = [0, -1, None, " ", "", "invalid_guild_id"]
    expected_response = "Error setting city: Invalid guild ID provided"
    for bad_guild_id in bad_guild_ids:
      response = await weatherFunctions.setCity(city, bad_guild_id)
      self.assertEqual(expected_response, response)

  # Testing valid unit inputs
  async def test_setUnits_validUnits(self):
    units = ["imperial", "metric"]
    for unit_sys in units:
      expected_response = f"Units set to {unit_sys}"
      response = await weatherFunctions.setUnits(unit_sys, TEST_GUILD_ID)
      self.assertEqual(expected_response, response)

  # Testing invalid unit inputs
  async def test_setUnits_invalidUnits(self):
    units = ["fake_system", " ", "", None]
    expected_response = "Error setting units: Invalid unit system"
    for unit_sys in units:
      response = await weatherFunctions.setUnits(unit_sys, TEST_GUILD_ID)
      self.assertEqual(expected_response, response)

  # Testing valid guild_id inputs
  async def test_setUnits_validGuildId(self):
    unit_sys = "imperial"
    expected_response = f"Units set to {unit_sys}"
    response = await weatherFunctions.setUnits(unit_sys, TEST_GUILD_ID)
    self.assertEqual(expected_response, response)

  # Testing invalid guild_id inputs
  async def test_setUnits_invalidGuildIds(self):
    unit_sys = "imperial"
    bad_guild_ids = [0, -1, None, " ", "", "invalid_guild_id"]
    expected_response = "Error setting city: Invalid guild ID provided"
    for bad_guild_id in bad_guild_ids:
      response = await weatherFunctions.setUnits(unit_sys, bad_guild_id)
      self.assertEqual(expected_response, response)

  # Testing weather command with valid guild_id inputs
  async def test_weather_validGuildId(self):
    city = "Lisbon"
    response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
    expected_response = f"Location set to {city}"
    self.assertEqual(expected_response, response)
    response = await weatherFunctions.weather(TEST_GUILD_ID, WEATHER_API_KEY)
    expected_response = f"In ***{city}***, it's"
    self.assertIn(expected_response, response)

  # Testing weather command with invalid guild_id inputs
  async def test_weather_invalidGuildId(self):
    city = "Lisbon"
    response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
    expected_response = f"Location set to {city}"
    self.assertEqual(expected_response, response)
    response = await weatherFunctions.weather(-1, WEATHER_API_KEY)
    expected_response = "Error retrieving weather data: Invalid guild ID provided"
    self.assertEqual(expected_response, response)

  # Testing weather command with city not yet set for guild
  async def test_weather_newGuildNoCity(self):
    from time import time_ns
    random_guild_id = int(time_ns() / 1000)
    response = await weatherFunctions.weather(random_guild_id, WEATHER_API_KEY)
    expected_response = "Please set your city first with `=setCity <city>`"
    self.assertEqual(expected_response, response)
  
  # Testing weather command with valid weather api key
  async def test_weather_validWeatherKey(self):
    city = "Lisbon"
    response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
    expected_response = f"Location set to {city}"
    self.assertEqual(expected_response, response)
    response = await weatherFunctions.weather(TEST_GUILD_ID, WEATHER_API_KEY)
    expected_response = f"In ***{city}***, it's"
    self.assertIn(expected_response, response)

  # Testing weather command with invalid weather api key
  async def test_weather_invalidWeatherKey(self):
    city = "Lisbon"
    bad_weather_key = "invalid_weather_key"
    response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
    expected_response = f"Location set to {city}"
    self.assertEqual(expected_response, response)
    response = await weatherFunctions.weather(TEST_GUILD_ID, bad_weather_key)
    expected_response = "Error retrieving weather data: Invalid or no API key provided"
    self.assertEqual(expected_response, response)

if __name__ == '__main__':
    unittest.main()