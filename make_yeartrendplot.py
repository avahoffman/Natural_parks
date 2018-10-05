def make_yeartrendplot(result, top_result_time):
    #import matplotlib.pyplot as plt
    import numpy as np
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.plotting import figure
    from bokeh.models import Range1d, LinearAxis
    import datetime

    visitors = np.exp(result['pred'])

    #define different axis labs, for visibility
    if max(visitors) > 500000:
        breaks = [10000, 50000, 100000, 500000, 1000000]
        overrides = {10000: '10k', 50000: '50k',100000: '100k',500000: '500k',1000000: '1 million'}
    elif max(visitors) > 100000:
        breaks = [10000, 50000, 100000, 500000]
        overrides = {10000: '10k', 50000: '50k',100000: '100k',500000: '500k'}
    elif max(visitors) > 50000:
        breaks = [10000, 25000, 50000, 75000, 100000]
        overrides = {10000: '10k', 25000: '25k', 50000: '50k', 75000: '75k',100000: '100k'}
    elif max(visitors) <= 50000:
        breaks = [1000, 5000, 10000, 25000, 50000]
        overrides = {1000: '1k', 5000: '5k', 10000: '10k', 25000: '25k', 50000: '50k'}
    
    dates_in_dt = np.array(result['date'], dtype=np.datetime64)
    top_in_dt = np.array(top_result_time, dtype=np.datetime64)
    # index top result for plotting
    ti=np.where(dates_in_dt == top_in_dt)[0]


    # def make_yeartrendplot(SELECTED_PARK):
    # plot a yearly trend
    plot = figure(y_range=( min(visitors)-1000,max(visitors)+1000), x_axis_type='datetime', plot_width=650, plot_height=300)
    plot.xaxis.axis_label = 'Month / Year'
    plot.yaxis.axis_label = 'Number of Visitors'
    plot.line(result['date'], visitors, color="black",legend = 'visitors', line_width=3)
    plot.yaxis.ticker = breaks
    plot.yaxis.major_label_overrides = overrides
    # Create 2nd y-axis
    plot.extra_y_ranges['temp'] = Range1d(start=0, end=110)
    plot.add_layout(LinearAxis(y_range_name='temp', axis_label='Temperature (°F)'), 'right')
    plot.line( x = result['date'], y = result['MaxT'], legend = 'max temp.', y_range_name = 'temp', color = 'orangered', line_width=3, line_dash='dotted')
    plot.line( x = result['date'], y = result['MinT'], legend = 'min temp.', y_range_name = 'temp', color = 'royalblue', line_width=3, line_dash='dotted')
    plot.toolbar_location = 'above'
    plot.quad(top=[max(visitors)+1000], bottom=[min(visitors)-1000], left=[dates_in_dt[ti][0]], right=[dates_in_dt[ti+1][0]], color='#22A784', fill_alpha = 0.2)
    plot.legend.border_line_width = 2
    plot.legend.border_line_color = "black"
    plot.legend.border_line_alpha = 0.5
    script, div = components(plot)
    return script, div