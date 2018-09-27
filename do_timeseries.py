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
	combined_maxtemp = NP_sub.rename(columns={'mergedate': 'ds', 'MaxT': 'y'})
	data_prophet_maxtemp = fbprophet.Prophet(changepoint_prior_scale=0.05, daily_seasonality=False, weekly_seasonality=False)
	data_prophet_maxtemp.fit(combined_maxtemp)
	data_forecast_maxtemp = data_prophet_maxtemp.make_future_dataframe(periods=12 * 3, freq='M')
	data_forecast_maxtemp = data_prophet_maxtemp.predict(data_forecast_maxtemp)
	# minimum temperature
	combined_mintemp = NP_sub.rename(columns={'mergedate': 'ds', 'MinT': 'y'})
	data_prophet_mintemp = fbprophet.Prophet(changepoint_prior_scale=0.05, daily_seasonality=False, weekly_seasonality=False)
	data_prophet_mintemp.fit(combined_mintemp)
	data_forecast_mintemp = data_prophet_mintemp.make_future_dataframe(periods=12 * 3, freq='M')
	data_forecast_mintemp = data_prophet_mintemp.predict(data_forecast_mintemp)
	# cleaning
	predicted_vals = data_forecast.drop(data_forecast.index[:len(data_forecast)-36])
	predicted_vals = predicted_vals.loc[:,['ds','yhat']]
	predicted_vals['date'] = predicted_vals['ds'].apply(lambda x: x + timedelta(days=1))
	predicted_vals_maxtemp = data_forecast_maxtemp.drop(data_forecast_maxtemp.index[:len(data_forecast_maxtemp)-36])
	predicted_vals_maxtemp = predicted_vals_maxtemp.loc[:,['ds','yhat']]
	predicted_vals_mintemp = data_forecast_mintemp.drop(data_forecast_mintemp.index[:len(data_forecast_mintemp)-36])
	predicted_vals_mintemp = predicted_vals_mintemp.loc[:,['ds','yhat']]
	result_pre = pd.merge(predicted_vals, predicted_vals_maxtemp, on='ds')
	result_vals = pd.merge(result_pre, predicted_vals_mintemp, on='ds')
	result_vals['month'] = result_vals['date'].apply(lambda x: x.strftime('%B'))
	result_vals['year'] = result_vals['date'].apply(lambda x: x.strftime('%Y'))
	return result_vals