import os
import pickle

from bokeh.embed import components
from flask import Flask
from flask import render_template

from abautomator.visualizer import utils, RelDiffVisualizer, AbsDiffVisualizer

app = Flask(__name__)

@app.route('/')
@app.route('/relative')
def relative():

    vis = RelDiffVisualizer(_get_rel_source())
    layout = vis.get_layout()
    bokeh_script, bokeh_div = components(layout)
    return render_template(
        'index.html',
        bokeh_script=bokeh_script,
        bokeh_div=bokeh_div,
        )

def _get_rel_source():
    name = "proximity_analy"
    analy = pickle.load(
        open(os.path.join("..", "tests", "cache", f"{name}.p"), "rb" )
    )
    metric_order = ['n_entered_phone', 'pct_entered_phone', 'n_granted_contacts', 'pct_granted_contacts']
    cond_order = ['Video01', 'Carousel01', 'Carousel02', 'Carousel03', 'Carousel04']

    df = analy.get_rel_diff_confidence_intervals()

    df = utils.order_categories(df, metric_order, cond_order)
    return utils.convert_df_to_source(df)

@app.route('/absolute')
def absolute():

    vis = AbsDiffVisualizer(_get_abs_source())
    layout = vis.get_layout()
    bokeh_script, bokeh_div = components(layout)
    return render_template(
        'index.html',
        bokeh_script=bokeh_script,
        bokeh_div=bokeh_div,
    )

def _get_abs_source():
    name = "proximity_analy"
    analy = pickle.load(
        open(os.path.join("..", "tests", "cache", f"{name}.p"), "rb" )
    )
    metric_order = ['n_entered_phone', 'pct_entered_phone', 'n_granted_contacts', 'pct_granted_contacts']
    cond_order = ['Video01', 'Carousel01', 'Carousel02', 'Carousel03', 'Carousel04']

    df = analy.get_abs_diff_confidence_intervals()

    df = utils.order_categories(df, metric_order, cond_order)
    return utils.convert_df_to_source(df)