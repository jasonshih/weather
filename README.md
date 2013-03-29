UK vs Hobbitland Weather mini-app
=================================

Mini weather app to compare max/min + historical temperatures between Gatwick, UK vs Auckland, NZ.

Stack
-----
 * **Backend:** [Python + Django](https://www.djangoproject.com/), [MySQL](http://www.mysql.com)
 * **Frontend:** [Bootstrap](http://twitter.github.com/bootstrap/), [jQuery](http://jquery.com/), [HighCharts](http://www.highcharts.com/)
 * **Data:** [Wunderground.com](http://www.wunderground.com/)


Changelog
---------
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
    
* **v1.1** (29/3/13)
    * Reorganised code base


TODO:
-----

 * Get demo version online
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
* Comment code base
    
    
    
