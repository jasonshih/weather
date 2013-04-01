from django.db import models

class Weather(models.Model):
	date = models.CharField(max_length=20)
	nzmax = models.CharField(max_length=10)
	nzmin = models.CharField(max_length=10)
	ukmax = models.CharField(max_length=10)
	ukmin = models.CharField(max_length=10)
	nzhistmax = models.CharField(max_length=10)
	nzhistmin = models.CharField(max_length=10)
	ukhistmax = models.CharField(max_length=10)
	ukhistmin = models.CharField(max_length=10)
	
	def __unicode__(self):
		return self.date
