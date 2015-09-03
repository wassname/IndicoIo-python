#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from indicoio import config
from indicoio import sentiment

class TestVersioning(unittest.TestCase):
    def setUp(self):
        self.api_key = config.api_key

    def test_specify_version(self):
        test_data = ['Worst song ever', 'Best song ever']
        response = sentiment(test_data, api_key = self.api_key, version="1")
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 2)
        self.assertTrue(response[0] < .5)
        self.assertTrue(response[1] > .5)

if __name__ == "__main__":
    unittest.main()
