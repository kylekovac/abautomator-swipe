import os
import dill as pickle

from bokeh.embed import components
from flask import Flask
from flask import render_template

from abautomator.visualizer import RelDiffVisualizer, AbsDiffVisualizer
from abautomator.exp_config import PRIMARY_METRIC_LIST, SECONDARY_METRIC_LIST, GUARDRAIL_METRIC_LIST
from app import utils

app = Flask(__name__)

@app.route('/')
@app.route('/primary')
def primary():
    return render_specific_metrics(PRIMARY_METRIC_LIST, "primary metrics")


def render_specific_metrics(metric_list, metric_label):

    layouts = utils._get_layouts(RelDiffVisualizer, metric_list, metric_label)
    scripts, divs = [], []
    for layout in layouts:
        bokeh_script, bokeh_div = components(layout)
        scripts.append(bokeh_script)
        divs.append(bokeh_div)
    return render_template(
        'index.html',
        scripts=scripts,
        divs=divs,
        )

@app.route('/secondary')
def secondary():
    return render_specific_metrics(SECONDARY_METRIC_LIST, "secondary metrics")

@app.route('/guardrail')
def guardrail():
    return render_specific_metrics(GUARDRAIL_METRIC_LIST, "guardrail metrics")
