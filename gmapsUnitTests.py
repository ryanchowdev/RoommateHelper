from unittest import IsolatedAsyncioTestCase
import unittest
import gmapsFunctions

TEST_GUILD_ID = 1 #Going under assumption that no discord server has guild id of TESTID
class GmapsTests(IsolatedAsyncioTestCase):
  def test(self):
    self.assertTrue(True)

  # Testing valid places inputs
  def test_gmaps_validPlaces(self):
    places = ["Cafe", "Mexican Food", "Museums"]
    for place in places:
      response = gmapsFunctions.places(place.split(" "))
      p = place.replace(" ", "%20")
      expected_response = f"https://www.google.com/maps/search/?api=1&query={p}"
      self.assertEqual(expected_response, response)

  # Testing invalid places input
  def test_gmaps_invalidPlace(self):
    place = ''
    response = gmapsFunctions.places([place])
    expected_response = "Please enter a query by `=places <query>`, ex: =places coffee shop"
    self.assertEqual(expected_response, response)

if __name__ == '__main__':
    unittest.main()