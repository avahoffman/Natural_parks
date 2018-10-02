def do_timeseries(NP_sub):
	import pandas as pd
	import fbprophet
	from datetime import datetime, timedelta
	# prophet modeling for visitors # 
	combined_vals = NP_sub.rename(columns={'mergedate': 'ds', 'RecreationVisits': 'y'})
	data_prophet = fbprophet.Prophet(changepoint_prior_scale=0.05, daily_seasonality=False, weekly_seasonality=False)
	data_prophet.fit(combined_vals)
	data_forecast = data_prophet.make_future_dataframe(periods=12 * 3, freq='M')
	data_forecast = data_prophet.predict(data_forecast)
	# maximum temperature
	combined_maxtemp = combined_vals.loc[:,('Month','MaxT')]
	combined_maxtemp = combined_maxtemp.groupby(['Month']).mean()
	combined_maxtemp = pd.concat([combined_maxtemp.reset_index(drop=True), combined_maxtemp.reset_index(drop=True), combined_maxtemp.reset_index(drop=True)], axis=0)
	# minimum temperature
	combined_mintemp = combined_vals.loc[:,('Month','MinT')]
	combined_mintemp = combined_mintemp.groupby(['Month']).mean()
	combined_mintemp = pd.concat([combined_mintemp.reset_index(drop=True), combined_mintemp.reset_index(drop=True), combined_mintemp.reset_index(drop=True)], axis=0)
	# cleaning
	predicted_vals = data_forecast.drop(data_forecast.index[:len(data_forecast)-36])
	predicted_vals = predicted_vals.loc[:,['ds','yhat']]
	predicted_vals['date'] = predicted_vals['ds'].apply(lambda x: x + timedelta(days=1))
	predicted_vals_maxtemp = combined_maxtemp.loc[:,['MaxT']]
	predicted_vals_mintemp = combined_mintemp.loc[:,['MinT']]
	result_vals = pd.concat([predicted_vals.reset_index(drop=True), predicted_vals_maxtemp.reset_index(drop=True), predicted_vals_mintemp.reset_index(drop=True)], axis=1)
	result_vals['month'] = result_vals['date'].apply(lambda x: x.strftime('%B'))
	result_vals['year'] = result_vals['date'].apply(lambda x: x.strftime('%Y'))
	return result_vals