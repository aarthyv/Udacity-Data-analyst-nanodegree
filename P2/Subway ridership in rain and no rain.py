# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:23:08 2016

@author: aarthy
"""

from ggplot import *
import pandas
df = pandas.read_csv('turnstile_weather_data.csv')
print ggplot(df, aes('ENTRIESn_hourly', fill = 'rain')) + geom_bar(binwidth = 100) + ylim(low = 0) + xlim(low = -1, high = 5000) + ggtitle('Ridership Rain (blue)/ No rain (red) ') + xlab('Hourly entries in bins of 100') + ylab('Ridership in each bin')