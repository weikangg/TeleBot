import datetime
import requests
import pandas as pd

# 2-hour weather forecast data
today = datetime.datetime.today() 
params = {"date": today.strftime("%Y-%m-%d")} # YYYY-MM-DD 

try:
	wx_forecast = requests.get('https://api.data.gov.sg/v1/environment/2-hour-weather-forecast', params=params)
	wx_forecast = wx_forecast.json()
except:
	print("System busy now. Try again awhile later.")

plotDf = pd.DataFrame(wx_forecast['area_metadata']).merge(pd.DataFrame(wx_forecast['items'][-1]['forecasts']).reset_index(), how='inner', left_on='name', right_on='area')
plotDf = plotDf[['area','forecast','label_location']]
print(plotDf[['area', 'forecast']])
