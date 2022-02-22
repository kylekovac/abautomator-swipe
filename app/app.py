import os
import pickle

# from bokeh.embed import components
from flask import Flask
from flask import render_template

from abautomator.visualizer import utils, RelDiffVisualizer

app = Flask(__name__)

@app.route('/')
def hello_world():
    # name = "inspiration_analy"
    # analy = pickle.load(
    #     open(os.path.join("..", "tests", "cache", f"{name}.p"), "rb" )
    # )
    # metric_order = ['n_entered_phone', 'pct_entered_phone', 'n_granted_contacts', 'pct_granted_contacts']
    # cond_order = ['Video01', 'Carousel01', 'Carousel02', 'Carousel03', 'Carousel04']

    # df = analy.get_rel_diff_confidence_intervals()

    # df = utils.order_categories(df, metric_order, cond_order)
    # source = utils.convert_df_to_source(df)
    # vis = RelDiffVisualizer(source)
    # layout = vis.get_layout()
    # script, div = components(layout)
    user = {'username': 'Miguel'}
    return render_template(
        'index.html',
        user=user,
        # script=script, div=div
        )