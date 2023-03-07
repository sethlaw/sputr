# base class for all unit test generators
import requests_raw
import unittest

from services.token_service import TokenService


class RawRequestsTest(unittest.TestCase):

    def __init__(self, config, report, url=None, request=None, payloads=None, DEBUG=False):
        self.report = report  # This is where we put results
        self.config = config
        self.url = url
        self.request = request
        self.payloads = payloads or []
        self.DEBUG = DEBUG

    def setUp(self):
        return

    # do setup

    def tearDown(self):
        return

    # do tear down

    def mockService(self):
        return

    # Send an HTTP GET Request, wrapper around python requests library.
    # Returns a Response object
    def rawrequest(self, url, request=None):
        if self.DEBUG:
            print("Raw Request: " + url)
            print("---------------------------------")
            print(request)
            print("---------------------------------")

        res = requests_raw.raw(url=url,data=request)
        return res
