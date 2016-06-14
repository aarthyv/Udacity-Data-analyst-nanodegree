from ggplot import *
import pandas
df = pandas.read_csv('turnstile_weather_data.csv')
print ggplot(df, aes('Hour','ENTRIESn_hourly', fill = 'rain')) + geom_bar() + ylim(low = 0) + xlim(low = -1) + ggtitle('Ridership over time of the day-Rain (blue)/ No rain (red) ') + xlab('Hour') + ylab('Ridership')