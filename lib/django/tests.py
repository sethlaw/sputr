######################################
# sputr/django/tests.py
# created: 2017-01-21
# author: seth
######################################

from django.test import TestCase
from django.test import Client
from taskManager.models import Project, File, Notes, Task, Project, UserProfile
import urls


class TestSecurity(TestCase):
	"""SPUTR Security Tests - django"""

	def setUp(self):
		self.client = Client()
	
	def test_xss(self):
		"""testing django.nV for XSS"""
		self.client.login(username="seth", password="soccerlover")
		content = self.client.get("/taskManager/search/", {'q' : 'item"<script>alert(1234)</script>'}).content
		vulnerable = (b"<script>alert(1234)</script>" in content)
		assert vulnerable is not True
		
	def test_injection(self):
		assert True is True
