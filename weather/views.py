from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse
from datetime import datetime, timedelta
from dateutil import rrule
from django.conf import settings
from django.core.cache import cache
import json
import time
import urllib2
from weather.models import Weather
from django.utils import simplejson
from django.core import serializers
from BeautifulSoup import BeautifulSoup
import sched, time


def test(request):
	temp = time.time()
	dates_dict = Weather.objects.all().values('date')
	dates = []
	for item in dates_dict:
		dates.append(int(item['date']))
	last_date_epoch = max(dates)/1000
	last_date = time.strftime("%Y%m%d", time.gmtime(last_date_epoch))
	current_date = time.strftime("%Y%m%d", time.gmtime(time.time()))
	
	the_dates = []
	hist_dates = []
	epoch_dates = []
	for dt in rrule.rrule(rrule.DAILY,
				dtstart = datetime.strptime(last_date, '%Y%m%d')+timedelta(days=1),
				until = datetime.strptime(current_date, '%Y%m%d')-timedelta(days=1)):
		epoch_dates.append(int(time.mktime(time.strptime(dt.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))) - time.timezone)
		the_dates.append(dt.strftime('%Y%m%d'))
		hist_dates.append(dt.strftime('%Y/%m/%d'))
	
	i = 0
	api_count = 0
	for new_day in the_dates:
		api_count+=2
		if api_count > 10:
			time.sleep(65)
			api_count = 0
		
		epoch_day = epoch_dates[i]
		hist_day = hist_dates[i]
		i += 1
		print hist_day
		
		UK_url = 'http://api.wunderground.com/api/0f54192d6585cd65/history_' + new_day + '/q/EGKK.json'
		NZ_url = 'http://api.wunderground.com/api/0f54192d6585cd65/history_' + new_day + '/q/NZAA.json'
		UK_hist_url = 'http://www.wunderground.com/history/airport/EGKK/' + hist_day + '/PlannerHistory.html?view=HistoryForToday'
		NZ_hist_url = 'http://www.wunderground.com/history/airport/NZAA/' + hist_day + '/PlannerHistory.html?view=HistoryForToday'
		
		# Access UK historical data
		f = urllib2.urlopen(UK_hist_url)
		html_string = f.read()
		f.close()
		UK_parsed_html = BeautifulSoup(html_string)
		
		# Access NZ historical data
		f = urllib2.urlopen(NZ_hist_url)
		html_string = f.read()
		f.close()
		NZ_parsed_html = BeautifulSoup(html_string)
		
		# Access UK data
		f = urllib2.urlopen(UK_url)
		json_string = f.read()
		parsed_json = json.loads(json_string)
		UK_history = parsed_json['history']
		f.close()
		
		# Access NZ data
		f = urllib2.urlopen(NZ_url)
		json_string = f.read()
		parsed_json = json.loads(json_string)
		NZ_history = parsed_json['history']
		f.close()
		
		UK_mintemp = UK_history['dailysummary'][0]['mintempm']
		UK_maxtemp = UK_history['dailysummary'][0]['maxtempm']
		NZ_mintemp = NZ_history['dailysummary'][0]['mintempm']
		NZ_maxtemp = NZ_history['dailysummary'][0]['maxtempm']
		
		UK_hist_max = int(UK_parsed_html.findAll("span", "nobr")[0].contents[0].contents[0])
		UK_hist_min = int(UK_parsed_html.findAll("span", "nobr")[2].contents[0].contents[0])
		NZ_hist_max = int(NZ_parsed_html.findAll("span", "nobr")[0].contents[0].contents[0])
		NZ_hist_min = int(NZ_parsed_html.findAll("span", "nobr")[2].contents[0].contents[0])
		
		addtoDB = Weather(date=epoch_day*1000, nzmax=NZ_maxtemp, nzmin=NZ_mintemp, ukmax=UK_maxtemp, ukmin=UK_mintemp, nzhistmax=NZ_hist_max, nzhistmin=NZ_hist_min, ukhistmax=UK_hist_max, ukhistmin=UK_hist_min)
		addtoDB.save()
		
		#print new_day, epoch_day, "UK: ", UK_mintemp, UK_maxtemp
		#print new_day, epoch_day, "NZ: ", NZ_mintemp, NZ_maxtemp

	
	return render(request, 'test.html')
	
def data(request):
	if request.is_ajax():
		QS = Weather.objects.all()
		response = serializers.serialize("json", QS)
		return HttpResponse(response, content_type="application/json")
		
		
		
		