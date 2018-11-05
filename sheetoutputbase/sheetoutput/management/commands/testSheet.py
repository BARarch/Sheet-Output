import httplib2
from django.conf import settings

from googleapiclient.discovery import build
from django.core.management.base import BaseCommand, CommandError
from parsebot.models import Article
from sheetoutput.models import CredetialsModel

from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.client import flow_from_clientsecrets


class Command(BaseCommand):
	help = 'Pulls feeds from in the group assigned to the app'

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		storage = get_storage_for_super()

		print('got storage object...')
		cred = storage.get()

		if cred is None:
			print('bad object')
			
		elif cred.invalid == True:
			print('cred is invalid')
		else:	
			print('cred is valid...')


			http = cred.authorize(httplib2.Http())
			discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
							'version=v4')
			service = build('sheets', 
							'v4', 
							http=http,
							discoveryServiceUrl=discoveryUrl)

			spreadsheet_id = '1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ'
			value_input_option = 'RAW'
			rangeName = 'DjangoTest!A' + '4'
			values = [['hello world from django management command server off']]
			body = {
				  'values': values
			}
			
			result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
															valueInputOption=value_input_option, body=body).execute()
			print('DONE')

		return 



def get_storage_for_super():
	return DjangoORMStorage(    CredetialsModel, 
								'user_id', 
								1, 
								'credential')
