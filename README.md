UK vs Hobbitland Weather mini-app
=================================

Online demo: [http://comparetheweather.herokuapp.com/](http://comparetheweather.herokuapp.com/)

Mini weather app to compare max/min + historical temperatures between Gatwick, UK vs Auckland, NZ.

Stack
-----
 * **Backend:** [Python + Django](https://www.djangoproject.com/), [MySQL](http://www.mysql.com)
 * **Frontend:** [Bootstrap](http://twitter.github.com/bootstrap/), [jQuery](http://jquery.com/), [HighCharts](http://www.highcharts.com/)
 * **Data:** [Wunderground.com](http://www.wunderground.com/)


Changelog
---------
* **v1.1** (2/4/13)
    * Reorganised & commented code base
    * Github banner added
    * Started to integrate deployment & production best practises, workflows & adaptations:
        * requirements.txt split out into dev, prod, test
        * settings.py split out into settings module with dev, prod, test (specified at runtime using "--settings=weather.settings.prod" flag)
        * Fixed issue with ALLOWED_HOSTS
        * Pushed to Heroku, using gunicorn
        * Serving static files works fine in dev mode (locally & on Heroku) but not using gunicorn in production
        * Added stopgap in urls.py to serve static files, until files can be served from S3
    * Demo version now online at [http://comparetheweather.herokuapp.com/](http://comparetheweather.herokuapp.com/)
    * *Issue:* Sleep timer causing Heroku timeout
        * Sleep timer implemented due to Wunderground API restrictions, causes Heroku to time out (still adds 5 records to database, times out on sleep)
        * Would be fixed by daily background process grabbing the API data; might be possible to scrape or use different source?
    * *Issue:* Looks like HTML is scraping fahrenheit instead of celsius now from the Wundeground almanac

* **v1.0** (29/3/13)
    * Working version, uploaded to GitHub
    * Displays max/min current & historical temperatures for UK (Gatwick) & NZ (Auckland)
    * Uses HighCharts interface for displaying data
    * Records are cached into a MySQL database upon pageload
    * Actual & historical averages are pulled from the Wunderground weather data API
    * Forecasts are scraped from the Wunderground forecast HTML
    * Includes [ShareThis](http://sharethis.com/) sharebar
    * Includes [Disqus](http://disqus.com/) comments
    * Locally hosted
    

TODO:
-----

 * Share it out
 * Align epoch times for forecast
 * Add historical temps for forecast
 * Possible to do 5 day forecast?
 * Add a highcharts data selector
 * Add in previous older historical data
 * Default displays last month only
 * Daily data collection script:
    - Currently data is pulled into the database from wunderground API at runtime
    - Wunderground API has some limits (i.e. 10 calls / minute), which means that if more than ~4 days have passed since someone last looked at this mini-app, there's a one-minute sleep timer built into the script to ensure I don't run over my API limit
    - This can make page load VERY slow (i.e. if 2 weeks have passed, it can take up to 5 minutes)
    - Therefore, add python script on server that runs every day at e.g. 00:01 (or maybe 01:00 to be safe) pulling in data into database
    
    
    
