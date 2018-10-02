# essential for interface
# https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50
from flask import Flask, request, render_template
# essential scripts
from get_parkdat import get_parkdat
from do_timeseries import do_timeseries
from make_yeartrendplot import make_yeartrendplot
from euclidean_dist import euclidean_dist
#modules
import pandas as pd
from datetime import datetime, timedelta
import io
import base64
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
	app.logger.info('starting website code')
	# user inputs
	SELECTED_PARK = request.form['location']
	SELECTED_MAXTEMP = int(request.form['max_temp_input'])
	SELECTED_MINTEMP = int(request.form['min_temp_input'])
	crowd_importance = int(request.form['crowd_importance'])
	min_importance = int(request.form['min_importance'])
	max_importance = int(request.form['max_importance'])
	app.logger.info('input complete')
	# query sql
	app.logger.info('querying sql')
	NP_sub = get_parkdat(SELECTED_PARK)
	app.logger.info('sql done')
	# subset
	app.logger.info('subsetting data')
	NP_sub['mergedate'] = pd.to_datetime(NP_sub.assign(Day=1).loc[:, ['Year','Month','Day']])
	app.logger.info('subset complete')
	# make a dictionary for website
	site_dic = pd.Series(NP_sub.website.values,index=NP_sub.ParkName).to_dict()
	website = site_dic[SELECTED_PARK]
	# make the yearly trend plot
	app.logger.info('plotting')
	plotscript = []
	plotdiv = []
	plotscript, plotdiv = make_yeartrendplot(NP_sub)
	app.logger.info('plotting complete')
	#
	# prophet modeling for visitors # 
	app.logger.info('begin time series')
	result_vals = do_timeseries(NP_sub)
	app.logger.info('time series complete')
	#
	# calculate distances
	app.logger.info('begin calculate euclidean distances')
	dist_results = euclidean_dist(result_vals,crowd_importance,min_importance,max_importance,SELECTED_MAXTEMP,SELECTED_MINTEMP)
	month_rec = dist_results[0]
	year_rec = dist_results[1]
	actual_max = round(dist_results[2],2)
	actual_min = round(dist_results[3],2)
	app.logger.info('dist complete')
	# provide output
	MESSAGE_HEAD = "We recommend visiting "+SELECTED_PARK+" in "
	MESSAGE_MID = month_rec+" "+year_rec
	MESSAGE_TAIL = ""
	MESSAGE_2 = "At this time, "+SELECTED_PARK+" should be between "+str(actual_min)+" F (minimum) and "+str(actual_max)+" F (maximum)."
	INPUT_MESSAGE = "Your selected temperature range was "+str(SELECTED_MINTEMP)+" - "+str(SELECTED_MAXTEMP)+" F."
	return render_template('results.html', MESSAGE_HEAD=MESSAGE_HEAD, MESSAGE_MID=MESSAGE_MID, MESSAGE_TAIL=MESSAGE_TAIL, MESSAGE_2=MESSAGE_2, INPUT_MESSAGE=INPUT_MESSAGE, plotscript = plotscript, plotdiv=plotdiv, website=website)

if __name__ == '__main__':
    app.run()
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)