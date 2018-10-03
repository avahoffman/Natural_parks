# essential for interface
# https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50
from flask import Flask, request, render_template
#modules
import pandas as pd
import datetime
import scipy
from sklearn import preprocessing
import os
import sys
import logging

app = Flask(__name__)

@app.route('/')    
@app.route('/index', methods=['GET', 'POST'])
def index():
    # define any variables down here to interface between the two pages, html on left and definition on right
    return render_template('index.html')
    
@app.route('/about', methods=['GET', 'POST'])
def about():
    # define any variables down here to interface between the two pages, html on left and definition on right
    return render_template('about.html')

@app.route('/results', methods=['GET','POST'])
def results():
	#
	# user inputs
	SELECTED_PARK = request.form['location']
	SELECTED_MAXTEMP = int(request.form['max_temp_input'])
	SELECTED_MINTEMP = int(request.form['min_temp_input'])
	crowd_importance = int(request.form['crowd_importance'])
	min_importance = int(request.form['min_importance'])
	max_importance = int(request.form['max_importance'])
	#
	# which model was best?
	m = pd.read_csv("pre_validation.csv", low_memory=False)
	sub = m[m.loc[:,('ParkName')] == SELECTED_PARK ]
	if sub.iloc[1,6] < sub.iloc[1,7]:
		method = "fb_prophet"
	else:
		method = "arima"
	#
	# predicted data
	d = pd.read_csv("timeseries_predictions_dat.csv", low_memory=False)
	if method == "fb_prophet":
		d.rename(columns={'yhat_fb': 'pred'}, inplace=True)
	else:
		d.rename(columns={'yhat_arima': 'pred'}, inplace=True)
	#
	# website dictionary
	site_dic = pd.Series(d.site.values,index=d.ParkName).to_dict()
	website = site_dic[SELECTED_PARK]
	# drop 2018
	d['date'] = d['date'].astype('datetime64[ns]')
	result = d.drop(d[d['date'] < '2018-11-01' ].index)
	cos_df = result.loc[:,('pred','MaxT',"MinT")]
	crowd_imp = crowd_importance
	crowd = 10-crowd_imp
	min_imp = min_importance
	max_imp = max_importance
	least_crowded = min(result['pred'])
	most_crowded = max(result['pred'])
	optimal_crowd = least_crowded + (((most_crowded - least_crowded) / 10 )*crowd)
	weights = [crowd_importance,max_importance,min_importance]
	cos_array = cos_df.values
	ss = preprocessing.StandardScaler().fit(cos_array)
	features_std = ss.transform(cos_array)
	user_input = pd.DataFrame([[ optimal_crowd, SELECTED_MAXTEMP, SELECTED_MINTEMP]], columns=('yhat_x','MaxT','MinT')) 
	user_input = user_input.values
	user_input = ss.transform(user_input)
	euc_dist= scipy.spatial.distance.cdist(user_input, features_std, metric='euclidean', w=weights)[0]
	topmatch = sorted(enumerate(euc_dist), key = lambda x: x[1], reverse = False)[0]
	top_result = result.iloc[topmatch[0]]
	top_result_time = top_result[3]
	top_result_max = round(top_result[4],1)
	top_result_min = round(top_result[5],1)
	month_rec = top_result_time.strftime('%B')
	year_rec = top_result_time.strftime('%Y')
	if year_rec == '2020':
		year_msg = "declining"
	else:
		year_msg = "increasing"
	crowd_msg = "Adjusting preferences can help make your ideal visit less crowded."
	# provide output
	MESSAGE_MID = month_rec+" "+year_rec
	return render_template('results.html', MESSAGE_MID=MESSAGE_MID, website=website, year_msg=year_msg, top_result_max=top_result_max, top_result_min=top_result_min,SELECTED_PARK=SELECTED_PARK,SELECTED_MAXTEMP=SELECTED_MAXTEMP,SELECTED_MINTEMP=SELECTED_MINTEMP, crowd_msd=crowd_msg)

if __name__ == '__main__':
    app.run()
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)