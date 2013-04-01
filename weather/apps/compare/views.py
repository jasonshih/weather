from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse
from datetime import datetime, timedelta
from dateutil import rrule
from django.conf import settings
from django.core.cache import cache
import json
import time
import urllib2
from weather.apps.compare.models import Weather
from django.utils import simplejson
from django.core import serializers
from bs4 import BeautifulSoup
import sched, time


# View 'test' 
def test(request):
	temp = time.time() # Find current time (object)
	dates_dict = Weather.objects.all().values('date') # Retrieve list of all current dates listed in the database
	dates = [] # Init empty dates dictionary
	for item in dates_dict: # For each date (in database), insert the timestamp into dates dictionary as an integer
		dates.append(int(item['date']))
	last_date_epoch = max(dates)/1000 # Find most recent date present in database
	last_date = time.strftime("%Y%m%d", time.gmtime(last_date_epoch)) # Format last date as e.g. 20132103
	current_date = time.strftime("%Y%m%d", time.gmtime(time.time()))  # Format current date as 20132903
	
	# Init dictionaries of dates in various formats (for different APIs)
	the_dates = []
	hist_dates = []
	epoch_dates = []
	# Iterate over a for loop built as all the days inbetween last date in database & current date
	for dt in rrule.rrule(rrule.DAILY,
				dtstart = datetime.strptime(last_date, '%Y%m%d')+timedelta(days=1),
				until = datetime.strptime(current_date, '%Y%m%d')-timedelta(days=1)):
		# Take dt object, format as timestamp -> time.strptime object -> time.mktime obkect -> int
		epoch_dates.append(int(time.mktime(time.strptime(dt.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))) - time.timezone)
		# Reformat time in two different ways for Wunderground APIs (i.e. current & historical conditions)
		the_dates.append(dt.strftime('%Y%m%d'))
		hist_dates.append(dt.strftime('%Y/%m/%d'))
	
	
	# Iterate over all the new dates for which we need to obtain actuals & historical average conditions
	i = 0 # Using var i to select correct date out of the dates array
	api_count = 0 # Count API calls (API limit of 10 calls per minute)
	for new_day in the_dates:
		api_count+=2 # Two API calls about to be made
		if api_count > 10: # If about to exceed limit of 10 calls, sleep for ~1 minute, then reset counter
			time.sleep(65)
			api_count = 0
		
		epoch_day = epoch_dates[i] # Specify relevant date in correct format
		hist_day = hist_dates[i]
		i += 1
		
		# These are the URLs to use for the API call, injected with the relevant date of interest; receiving data back as JSON
		# ICAO airport codes used for weather conditions (historical & almanac data available for airports worldwide)
		# Gatwick, UK airport code = EGKK; Auckland, NZ airport code = NZAA
		UK_url = 'http://api.wunderground.com/api/0f54192d6585cd65/history_' + new_day + '/q/EGKK.json' # UK conditions for given day (API call)
		NZ_url = 'http://api.wunderground.com/api/0f54192d6585cd65/history_' + new_day + '/q/NZAA.json' # NZ conditions for given day (API call)
		UK_hist_url = 'http://www.wunderground.com/history/airport/EGKK/' + hist_day + '/PlannerHistory.html?view=HistoryForToday' # UK almanac (HTML page)
		NZ_hist_url = 'http://www.wunderground.com/history/airport/NZAA/' + hist_day + '/PlannerHistory.html?view=HistoryForToday' # NZ almanac (HTML page)
		
		# Access UK historical data (scraping HTML)
		f = urllib2.urlopen(UK_hist_url) # Open connection to HTML page
		html_string = f.read() # Read the html, save as string
		f.close()  # Close the connection
		UK_parsed_html = BeautifulSoup(html_string) # Parse HTML string into BeautifulSoup object
		
		# Access NZ historical data (scraping HTML)
		f = urllib2.urlopen(NZ_hist_url) # Open connection to HTML page
		html_string = f.read() # Read html, save as string
		f.close() # Close the connection
		NZ_parsed_html = BeautifulSoup(html_string) # Parse HTML string into BeautifulSoup object
		
		# Access UK data (API call)
		f = urllib2.urlopen(UK_url) # Open connection to Wunderground API
		json_string = f.read() # Read JSON data into string
		f.close() # Close the connection
		parsed_json = json.loads(json_string) # Parse JSON string into json object
		UK_history = parsed_json['history'] # Extract 'history' part of the json

		
		# Access NZ data (API call)
		f = urllib2.urlopen(NZ_url) # Open connection to Wunderground API
		json_string = f.read() # Read JSON data into string
		f.close() # Close connection
		parsed_json = json.loads(json_string) # Parse JSON string into json object
		NZ_history = parsed_json['history'] # Extract 'history' part of the json
		
		# Extract actual max/min integers from the JSON histories
		UK_mintemp = UK_history['dailysummary'][0]['mintempm']
		UK_maxtemp = UK_history['dailysummary'][0]['maxtempm']
		NZ_mintemp = NZ_history['dailysummary'][0]['mintempm']
		NZ_maxtemp = NZ_history['dailysummary'][0]['maxtempm']
		
		# Extract historical average max/mins integers from the BS html objects
		UK_hist_max = int(UK_parsed_html.findAll("span", "nobr")[0].contents[0].contents[0])
		UK_hist_min = int(UK_parsed_html.findAll("span", "nobr")[2].contents[0].contents[0])
		NZ_hist_max = int(NZ_parsed_html.findAll("span", "nobr")[0].contents[0].contents[0])
		NZ_hist_min = int(NZ_parsed_html.findAll("span", "nobr")[2].contents[0].contents[0])
		
		# Specify a new Weather model record
		addtoDB = Weather(date=epoch_day*1000, nzmax=NZ_maxtemp, nzmin=NZ_mintemp, ukmax=UK_maxtemp, ukmin=UK_mintemp, nzhistmax=NZ_hist_max, nzhistmin=NZ_hist_min, ukhistmax=UK_hist_max, ukhistmin=UK_hist_min)
		addtoDB.save() # Save record to database
		
	
	return render(request, 'test.html') # Render test.html, nothing to inject...!
	



# View 'data' takes the ajax call, selects all the Weather records from the database	
def data(request):
	if request.is_ajax(): # Check call is ajax
		QS = Weather.objects.all() # Select all weather records
		response = serializers.serialize("json", QS) # Serialise as JSON
		return HttpResponse(response, content_type="application/json") # Return JSON response
		
		
		
		