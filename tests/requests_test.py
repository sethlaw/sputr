# base class for all unit test generators
import requests
import unittest

from services.token_service import TokenService


class RequestsTest(unittest.TestCase):

    def __init__(self, config, report, domain=None, creds=None, csrf=None, payloads=None, DEBUG=False):
        self.client = requests.Session()  # Each Test gets it's own session
        self.report = report  # This is where we put results
        self.config = config
        self.creds = creds or {}
        self.domain = domain or {}
        self.payloads = payloads or []
        self.csrf = csrf or {}
        self.DEBUG = DEBUG
        self.csrftoken = ""
        self.token_service = TokenService(self.csrf)
        if config['auth'] == 1:
            self.authenticate()

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
    def get(self, url, params=None, cookies=None, allow_redirects=True):
        params = params or {}
        cookies = cookies or {}
        if self.DEBUG:
            print(url + " : " + str(params) + " : " + str(cookies))
        res = self.client.get(url, params=params, cookies=cookies, allow_redirects=allow_redirects)
        tmptoken = self.token_service.get_csrf_token(res.text, self.DEBUG)
        if tmptoken != "":
            self.csrftoken = tmptoken
        return res

    def post(self, url, data=None, cookies=None, allow_redirects=True):
        data = data or {}
        cookies = cookies or {}
        if self.DEBUG:
            print(url + " : " + str(data) + " : " + str(cookies))
        if self.csrftoken:
            data[self.csrf['name']] = self.csrftoken
        res = self.client.post(url, data=data, cookies=cookies, allow_redirects=allow_redirects)
        tmptoken = self.token_service.get_csrf_token(res.text, self.DEBUG)
        if tmptoken:
            self.csrftoken = tmptoken
        return res

    def authenticate(self):
        if self.DEBUG:
            print("authenticating as " + self.creds['username']['value'] + " to " + self.domain['login_url'])
        res1 = self.get(self.domain['login_url'])
        if self.DEBUG:
            print("Status: " + str(res1.status_code))

        data = {self.creds['username']['name']: self.creds['username']['value'],
                self.creds['password']['name']: self.creds['password']['password']}
        res2 = self.post(self.domain['login_url'], data=data)
        if self.DEBUG:
            print("Status: " + str(res2.status_code))

        if res2.status_code != 200:
            print("Auth Failed")
            if self.DEBUG: print("Status 500: " + str(res2.content))

        res3 = self.get(self.domain['auth_url'], allow_redirects=False)
        if self.DEBUG:
            print("Status: " + str(res3.status_code))

        return res2.status_code
