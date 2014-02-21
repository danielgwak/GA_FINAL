import urllib
import os
import json
import time
import random
import numpy as np

years = [2009,2010,2011,2012,2013]
city = 'KNYC'

#Weather Underground only allows 18 months of data to be downloaded at once, so I am scraping separately for each of the last five calendar years

for year in years:
    time.sleep(.1+random.random())

    try:
        url = 'http://www.wunderground.com/history/airport/{0}/{1}/1/1/CustomHistory.html?dayend=31&monthend=12&yearend={2}&req_city=NA&req_state=NA&req_statename=NA&format=1'.format(city, year, year)
        print url
        data = urllib.urlopen(url).read()
        file = '%s_data.csv' % year
        f = open(file,'w')
        f.write('%s' % str(data))
        f.close()
        print 'wrote file %s' % file
        data = data.split('\n')

    except:
        print 'failed for %s' % year


