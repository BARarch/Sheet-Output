import os
import httplib2

from googleapiclient.discovery import build
from sheetoutput.models import CredetialsModel
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.conf import settings

import google.oauth2.credentials
import google.auth.transport.requests
import requests

from google_auth_oauthlib.flow import Flow


class Cred:

	SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
	CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
	APPLICATION_NAME = 'ParseBot-SheetOutput'
	REDIRECT_URI = 'http://localhost:8080/oath2callback'

	def __init__(self):
		self.storage = DjangoORMStorage(    CredetialsModel, 
											'user_id', 
											1, 
											'credential')
		self.cred = self.storage.get()
		self.check_token()
		return

	def get_cred(self):
		return self.cred

	def force_refresh(self):
		print('refreshing_token...')

		requestt = google.auth.transport.requests.Request()
		self.cred.refresh(requestt)
		self.storage.put(self.cred)
		return

	def check_token(self):
		if self.cred is None:
			print('Please Authenticate App with Browser')
			return
		if self.cred.expired == True:
			self.force_refresh()
		return

	def cred_to_dict(self):
		return {'token': credentials.token,
				'refresh_token': self.cred.refresh_token,
				'expiry': self.cred.expiry,
				'expired': self.cred.expired,
				'token_uri': self.cred.token_uri,
				'scopes': self.cred.scopes}

	def __str__(self):
		dictt = self.cred_to_dict()
		return 'Creds {\n' + '\n'.join(["\t'{}': {},".format(str(item), str(dictt[item])) for item in dictt]) + '\n}'

	def __repr__(self):
		dictt = self.cred_to_dict()
		return 'Creds {\n' + '\n'.join(["\t'{}': {},".format(str(item), str(dictt[item])) for item in dictt]) + '\n}'

