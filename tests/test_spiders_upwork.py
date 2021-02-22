import unittest
import os
import json
from argyle_challenge.spiders.upwork import UpworkSpider


class DummyResponse:
    body: str

    def __init__(self, body):
        self.body = body


class MyTestCase(unittest.TestCase):

    with open('sample_data.json') as json_file:
        sample_data = json.load(json_file)
    response = DummyResponse(json.dumps({'results': sample_data}))

    def test_get_data_from_api(self):
        upwork_spider = UpworkSpider()
        upwork_spider.get_data_from_api(self.response)
        self.assertEqual(len(upwork_spider.found_jobs), len(self.sample_data))


if __name__ == '__main__':
    unittest.main()
