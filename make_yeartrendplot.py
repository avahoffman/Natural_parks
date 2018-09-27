def make_yeartrendplot(NP_sub):
	from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
	from bokeh.models.glyphs import VBar
	from bokeh.plotting import figure
	from bokeh.embed import components
	from bokeh.models.sources import ColumnDataSource
	from bokeh.resources import CDN
	import pandas as pd
	import io
	import base64
	
	agg_park_dat = NP_sub.groupby( [ "Year"] )['RecreationVisits'].sum().to_frame(name = 'RecreationVisits').reset_index()
	plot = figure(x_range=(1978,2018), y_range=(min(agg_park_dat['RecreationVisits']),max(agg_park_dat['RecreationVisits'])))
	plot.xaxis.axis_label = 'Year'
	plot.yaxis.axis_label = 'Number of Visitors'
	plot.line(agg_park_dat['Year'], agg_park_dat['RecreationVisits'])
	plot.plot_width = 500
	plot.plot_height = 300
	script, div = components(plot)
	return script, div