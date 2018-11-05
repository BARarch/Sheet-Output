import os
#import logging
import httplib2

from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.conf import settings

from sheetoutput.models import CredetialsModel

from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.client import flow_from_clientsecrets

import google.oauth2.credentials
import google_auth_oauthlib.flow


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
APPLICATION_NAME = 'ParseBot-SheetOutput'

flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=SCOPES, redirect_uri='http://localhost:8080/oath2callback')
print('got flow')

@login_required
def authorize_fresh(request):
	flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
														request.user)
	print('We are generating a fresh token')
	print('we are using flow to generate token')
	print(flow.params)
	print(type(flow))
	authorize_url, state = flow.authorization_url(
		access_type='offline',
		include_granted_scopes='true')
	print('going to authorize... \nauthorize_url: {}'.format(str(authorize_url)))
	## If the flow is bad we might have to go to Google developers console
	## and get a new server to server secret for this django.
	return HttpResponseRedirect(authorize_url)

# Create your views here.
@login_required
def authorize(request):
	print(request.user)
	print(type(request.user))

	storage = DjangoORMStorage( CredetialsModel, 
								'user_id', 
								request.user, 
								'credential')
	
	print('got storage object...')
	cred = storage.get()

	if cred is None or cred.invalid == True:
		flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
														request.user)
		print('we have not valid credential stored')
		print('we are using flow to generate token')
		print(flow.params)
		print(type(flow))
		authorize_url, state = flow.authorization_url(
			access_type='offline',
			include_granted_scopes='true')
		print('going to authorize... \nauthorize_url: {}'.format(str(authorize_url)))
		## If the flow is bad we might have to go to Google developers console
		## and get a new server to server secret for this django.
		return HttpResponseRedirect(authorize_url)
	else:
		print(cred.to_json())

		print(type(cred))
		print(type(flow))
		http = httplib2.Http()
		http = cred.authorize(http)
		print('Credential Authorized')
		return render(request, 'sheetoutput/welcome.html', {})



@login_required
def auth_return(request):
	print(request.user)
	print(type(request.user))
	if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'].encode('UTF-8'), request.user):
		return HttpResponseBadRequest()
	
	cred = flow.step2_exchange(request.GET)
	storage = DjangoORMStorage(CredetialsModel, 'user_id', request.user, 'credential')
	storage.put(cred)
	print('credential done: check admin')
	return HttpResponseRedirect("/auth")

def get_the_user(request):
	storage = get_storage_for_super()

	print('got storage object...')
	cred = storage.get()

	# Is it the right one?
	if cred is None:
		print('bad object')
		return render(request, 'sheetoutput/message.html', {'outcome': 'the object was bad, there is no cred for this user'})

	elif cred.invalid == True:
		print('cred is invalid')
		return render(request, 'sheetoutput/message.html', {'outcome': 'the credential was valid'})
	else:
		print('it worked')
		return render(request, 'sheetoutput/message.html', {'outcome': 'it worked, this is the right user and the cred is valid'})

def reach_out_and_touch(request):
	storage = get_storage_for_super()

	print('got storage object...')
	cred = storage.get()

	if cred is None:
		print('bad object')
		return render(request, 'sheetoutput/message.html', {'outcome': 'the object was bad, there is no cred for this user'})

	elif cred.invalid == True:
		print('cred is invalid')
		return render(request, 'sheetoutput/message.html', {'outcome': 'the credential was not valid'})
	
	print('it worked')


	http = cred.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					'version=v4')
	service = build('sheets', 
					'v4', 
					http=http,
					discoveryServiceUrl=discoveryUrl)

	spreadsheet_id = '1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ'
	value_input_option = 'RAW'
	rangeName = 'DjangoTest!B' + '1'
	values = [['hello world from django view']]
	body = {
		  'values': values
	}
	
	result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
													valueInputOption=value_input_option, body=body).execute()


	return render(request, 'sheetoutput/message.html', {'outcome': 'it worked, this is the right user and the cred is valid the sheet has been touched'})


def get_storage_for_super():
	return DjangoORMStorage(    CredetialsModel, 
								'user_id', 
								1, 
								'credential')




	