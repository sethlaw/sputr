import requests
import re
from bs4 import BeautifulSoup


class TokenService():

    def __init__(self, csrf):
        self.csrf = csrf

    def login(self):
        return requests.post(self.csrf["auth_url"], data=self.creds, cookies=self.cookies)

    def get_session_cookie(self):
        response = self.login()
        return response.cookies.get_dict()[self.cookies["name"]]

    def get_auth_header(self):
        """
        This is for Auth based Authn Strategies
        """
        return

    def get_csrf_token(self, html, DEBUG=False):
        """
        Get specified header value
        """
        soup = BeautifulSoup(html, "lxml")
        c = soup.find('input', {"name": self.csrf['name']})
        if c:
            if re.match(self.csrf['pattern'], c['value']):
                return c['value']
        return ""
