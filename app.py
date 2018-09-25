# essential for interface
from flask import Flask, request, render_template
# essential for model, etc
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import fbprophet

app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # define any variables down here to interface between the two pages, html on left and definition on right
    return render_template('index.html')

@app.route('/results', methods=['GET','POST'])
def results():
	# read data
	NP = pd.read_csv("Visits_NP_NoAKHI.csv", low_memory=False)
	#
	#
	# user inputs
	SELECTED_PARK = request.form['location']
	#SELECTED_PARK = str(PARK.upper())
	SELECTED_TEMP = int(request.form['temp_input'])
	# subset main data
	NP_sub = NP[NP['ParkName'] == SELECTED_PARK ]
	NP_sub['mergedate'] = pd.to_datetime(NP_sub.assign(Day=1).loc[:, ['Year','Month','Day']])
	#
	# prophet modeling# 
	combined_vals = NP_sub.rename(columns={'mergedate': 'ds', 'RecreationVisits': 'y'})
	data_prophet = fbprophet.Prophet(changepoint_prior_scale=0.05, daily_seasonality=False, weekly_seasonality=False)
	data_prophet.fit(combined_vals)
	data_forecast = data_prophet.make_future_dataframe(periods=12 * 3, freq='M')
	data_forecast = data_prophet.predict(data_forecast)
	# temperature
	combined_temp = NP_sub.rename(columns={'mergedate': 'ds', 'MaxT': 'y'})
	data_prophet_temp = fbprophet.Prophet(changepoint_prior_scale=0.05, daily_seasonality=False, weekly_seasonality=False)
	data_prophet_temp.fit(combined_temp)
	data_forecast_temp = data_prophet_temp.make_future_dataframe(periods=12 * 3, freq='M')
	data_forecast_temp = data_prophet_temp.predict(data_forecast_temp)
	# cleaning
	predicted_vals = data_forecast.drop(data_forecast.index[:len(data_forecast)-36])
	predicted_vals = predicted_vals.loc[:,['ds','yhat']]
	predicted_vals['date'] = predicted_vals['ds'].apply(lambda x: x + timedelta(days=1))
	predicted_vals_temp = data_forecast_temp.drop(data_forecast_temp.index[:len(data_forecast_temp)-36])
	predicted_vals_temp = predicted_vals_temp.loc[:,['ds','yhat']]
	result_vals = pd.merge(predicted_vals, predicted_vals_temp, on='ds')
	result_vals['month'] = result_vals['date'].apply(lambda x: x.strftime('%B'))
	result_vals['year'] = result_vals['date'].apply(lambda x: x.strftime('%Y'))
	#
	#filter by user pref
	result_vals = result_vals.drop(result_vals[result_vals['yhat_y'] < SELECTED_TEMP ].index)
	result_vals = result_vals.drop(result_vals[result_vals['date'] < '2018-10-01' ].index)
	if len(result_vals) > 0:
		visit_list = result_vals['yhat_x']
		best = min(visit_list)
		month_rec = result_vals.loc[result_vals['yhat_x'] == best, 'month'].iloc[0]
		year_rec = result_vals.loc[result_vals['yhat_x'] == best, 'year'].iloc[0]
	else:
		month_rec = ''
		year_rec = ''
	return render_template('results.html', SELECTED_PARK=SELECTED_PARK, SELECTED_TEMP=SELECTED_TEMP, month_rec=month_rec, year_rec=year_rec)

if __name__ == '__main__':
    app.run()