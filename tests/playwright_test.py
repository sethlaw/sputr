#!/usr/bin/env python3
#####################################
# playwright_test.py
# Base class for Playwright-based tests
#####################################

import logging

logger = logging.getLogger(__name__)

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


class PlaywrightTest:
    """Base class for browser-based fuzz tests using Playwright.

    Same constructor signature as RequestsTest so the CLI can instantiate
    both identically. Manages Playwright lifecycle: headless Chromium,
    BrowserContext for session persistence, form-based authentication.
    """

    def __init__(self, config, report, domain=None, creds=None, csrf=None, payloads=None, DEBUG=False):
        if not HAS_PLAYWRIGHT:
            raise ImportError('playwright is not installed. Install with: pip install playwright && playwright install chromium')
        self.config = config
        self.report = report
        self.domain = domain or {}
        self.creds = creds or {}
        self.csrf = csrf or {}
        self.payloads = payloads or []
        self.DEBUG = DEBUG
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.console_errors = []
        self.setup_browser()
        if config.get('auth') == 1:
            self.authenticate()

    def setup_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.on('console', self._on_console)

    def _on_console(self, msg):
        if msg.type == 'error':
            self.console_errors.append(msg.text)

    def authenticate(self):
        login_url = self.domain.get('login_url', '')
        if not login_url:
            return
        if self.DEBUG:
            print("Playwright: authenticating to " + login_url)
        self.page.goto(login_url)

        username_name = self.creds.get('username', {}).get('name', 'username')
        username_value = self.creds.get('username', {}).get('value', '')
        password_name = self.creds.get('password', {}).get('name', 'password')
        password_value = self.creds.get('password', {}).get('password', '')

        try:
            self.page.fill('input[name="{}"]'.format(username_name), username_value)
            self.page.fill('input[name="{}"]'.format(password_name), password_value)
            self.page.click('input[type="submit"], button[type="submit"], button:has-text("Login"), button:has-text("Sign in")')
            self.page.wait_for_load_state('networkidle')
        except Exception as e:
            if self.DEBUG:
                print("Playwright auth error: " + str(e))

    def fill_and_submit(self, url, params):
        """Navigate to URL, fill form inputs with params, submit.

        Returns (page_content, status_code, console_errors).
        """
        self.console_errors = []
        response = self.page.goto(url)

        for name, value in params.items():
            try:
                self.page.fill('input[name="{}"], textarea[name="{}"]'.format(name, name), str(value))
            except Exception:
                try:
                    self.page.select_option('select[name="{}"]'.format(name), str(value))
                except Exception:
                    if self.DEBUG:
                        print("Could not fill field: " + name)

        try:
            self.page.click('input[type="submit"], button[type="submit"]')
            self.page.wait_for_load_state('networkidle')
        except Exception as e:
            if self.DEBUG:
                print("Submit error: " + str(e))

        content = self.page.content()
        status = response.status if response else 0
        errors = list(self.console_errors)
        return content, status, errors

    def navigate(self, url):
        """Simple GET navigation. Returns (content, status_code, console_errors)."""
        self.console_errors = []
        response = self.page.goto(url)
        self.page.wait_for_load_state('networkidle')
        content = self.page.content()
        status = response.status if response else 0
        errors = list(self.console_errors)
        return content, status, errors

    def teardown_browser(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def __del__(self):
        try:
            self.teardown_browser()
        except Exception:
            pass
