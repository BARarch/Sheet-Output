import httplib2
from django.conf import settings

from django.core.management.base import BaseCommand, CommandError
from sheetoutput.sheetoutput_classes.modelGS import SheetOutput



class Command(BaseCommand):
	help = 'Pulls feeds from in the group assigned to the app'

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		s = SheetOutput()
		s.say_hello()
		print('DONE: check sheet')
		