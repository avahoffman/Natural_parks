# essential for interface
# https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50
from flask import Flask, request, render_template
# essential for model, etc
from get_parkdat import get_parkdat
from do_timeseries import do_timeseries
from make_yeartrendplot import make_yeartrendplot
import pandas as pd
from datetime import datetime, timedelta
import io
import base64

app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # define any variables down here to interface between the two pages, html on left and definition on right
    return render_template('index.html')

@app.route('/results', methods=['GET','POST'])
def results():
	# user inputs
	SELECTED_PARK = request.form['location']
	#SELECTED_PARK = str(PARK.upper())
	SELECTED_MAXTEMP = int(request.form['max_temp_input'])
	SELECTED_MINTEMP = int(request.form['min_temp_input'])
	# subset main data
	#NP_sub = NP[NP['ParkName'] == SELECTED_PARK ]
	NP_sub = get_parkdat(SELECTED_PARK)
	NP_sub['mergedate'] = pd.to_datetime(NP_sub.assign(Day=1).loc[:, ['Year','Month','Day']])
	#
	# make the yearly trend plot
	plotscript = []
	plotdiv = []
	plotscript, plotdiv = make_yeartrendplot(NP_sub)
	#
	# prophet modeling for visitors # 
	result_vals = do_timeseries(NP_sub)
	#
	#filter by user pref
	result_vals = result_vals.drop(result_vals[result_vals['yhat_y'] > SELECTED_MAXTEMP ].index)
	result_vals = result_vals.drop(result_vals[result_vals['yhat'] < SELECTED_MINTEMP ].index)
	# remove 2018
	result_vals = result_vals.drop(result_vals[result_vals['date'] < '2018-10-01' ].index)
	if len(result_vals) > 0:
		visit_list = result_vals['yhat_x']
		best = min(visit_list)
		month_rec = result_vals.loc[result_vals['yhat_x'] == best, 'month'].iloc[0]
		year_rec = result_vals.loc[result_vals['yhat_x'] == best, 'year'].iloc[0]
		actual_min = round(result_vals.loc[result_vals['yhat_x'] == best, 'yhat'].iloc[0], 2)
		actual_max = round(result_vals.loc[result_vals['yhat_x'] == best, 'yhat_y'].iloc[0], 2)
		MESSAGE = "We recommend visiting "+str(SELECTED_PARK)+" in "+month_rec+" of "+str(year_rec)+" to avoid the crowds."
		MESSAGE_2 = "At this time, the minimum temperature at "+str(SELECTED_PARK)+" should be "+str(actual_min)+" F and the maximum temperature should be "+str(actual_max)+" F."
		INPUT_MESSAGE = "Your selected temperature range was "+str(SELECTED_MINTEMP)+" - "+str(SELECTED_MAXTEMP)+" F."
	else:
		month_rec = '---'
		year_rec = '---'
		actual_min = '---'
		actual_max = '---'
		MESSAGE = 'Your temperature cutoffs are too restrictive. Remember many of these parks get quite cold at night! Please adjust and try again.'
		MESSAGE_2 = '' 
		INPUT_MESSAGE = ''
	return render_template('results.html', MESSAGE=MESSAGE, MESSAGE_2=MESSAGE_2, INPUT_MESSAGE=INPUT_MESSAGE, plotscript = plotscript, plotdiv=plotdiv)

if __name__ == '__main__':
    app.run()