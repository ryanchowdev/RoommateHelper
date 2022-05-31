from unittest import IsolatedAsyncioTestCase
import unittest
import weatherFunctions

TEST_GUILD_ID = 1 #Going under assumption that no discord server has guild id of TESTID
class WeatherTests(IsolatedAsyncioTestCase):
  def test(self):
    self.assertTrue(True)

  # Testing valid city inputs
  def test_getWeather_validCities(self):
    cities = ["New York", "Amsterdam", "London"]
    unit_sys = "imperial"
    weather_api_key = "b21b205ea20945d9135435890e29249d"
    for city in cities:
      expected_response = f"In ***{city}***, it's"
      response = weatherFunctions.getWeather(city, unit_sys, weather_api_key)
      self.assertIn(expected_response, response)
      self.assertIn("°F", response)

  # Testing invalid city inputs
  def test_getWeather_invalidCities(self):
    cities = ["Fake City", "Bruh"]
    unit_sys = "imperial"
    weather_api_key = "b21b205ea20945d9135435890e29249d"
    for city in cities:
      expected_response = "Error retrieving weather data: HTTP error 404"
      response = weatherFunctions.getWeather(city, unit_sys, weather_api_key)
      self.assertEqual(expected_response, response)

  # Testing valid unit inputs
  def test_getWeather_validUnits(self):
    city = "New York"
    unit_sys = "imperial"
    weather_api_key = "b21b205ea20945d9135435890e29249d"
    expected_response = f"In ***{city}***, it's"
    response = weatherFunctions.getWeather(city, unit_sys, weather_api_key)
    self.assertIn(expected_response, response)
    self.assertIn("°F", response)
    unit_sys = "metric"
    expected_response = f"In ***{city}***, it's"
    response = weatherFunctions.getWeather(city, unit_sys, weather_api_key)
    self.assertIn(expected_response, response)
    self.assertIn("°C", response)

  # Testing invalid unit inputs
  def test_getWeather_invalidUnits(self):
    city = "New York"
    unit_sys = "fake_system"
    weather_api_key = "b21b205ea20945d9135435890e29249d"
    expected_response = "Error retrieving weather data: invalid unit system"
    response = weatherFunctions.getWeather(city, unit_sys, weather_api_key)
    self.assertEqual(expected_response, response)

  # Testing valid city inputs
  async def test_setCity(self):
    cities = ["New York", "Amsterdam", "London"]
    for city in cities:
      expected_response = f"Location set to {city}"
      response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
      self.assertEqual(expected_response, response)

  # Testing valid unit inputs
  async def test_setUnits(self):
    units = ["imperial", "metric"]
    for unit_sys in units:
      expected_response = f"Units set to {unit_sys}"
      response = await weatherFunctions.setUnits(unit_sys, TEST_GUILD_ID)
      self.assertEqual(expected_response, response)

  # Testing weather command with city already set for guild
  async def test_weather_existingGuild(self):
    city = "Lisbon"
    weather_api_key = "b21b205ea20945d9135435890e29249d"
    response = await weatherFunctions.setCity(city, TEST_GUILD_ID)
    self.assertEqual(expected_response, response)
    expected_response = f"Location set to {city}"
    response = weatherFunctions.weather(TEST_GUILD_ID, weather_api_key)
    expected_response = f"In ***{city}***, it's"

  # Testing weather command with city not yet set for guild
  async def test_weather_existingGuild(self):
    weather_api_key = "b21b205ea20945d9135435890e29249d"
    response = await weatherFunctions.weather(999999, weather_api_key)
    expected_response = "Please set your city first with `=setCity <city>`"
    self.assertEqual(expected_response, response)

if __name__ == '__main__':
    unittest.main()