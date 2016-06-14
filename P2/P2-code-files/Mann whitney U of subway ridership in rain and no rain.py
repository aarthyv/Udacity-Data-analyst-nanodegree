import pandas as pd
import numpy as np
import scipy.stats
filename = "turnstile_weather_data.csv"
turnstile_weather = pd.read_csv(filename)
without_rain = turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly'].reset_index(drop=True)
with_rain = turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly'].reset_index(drop=True)
with_rain_mean = np.mean(with_rain)
without_rain_mean = np.mean(without_rain)
result = scipy.stats.mannwhitneyu(with_rain, without_rain)
print with_rain_mean, without_rain_mean, result