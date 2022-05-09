import os
import dill as pickle

from bokeh.embed import components
from flask import render_template

from abautomator.visualizer import utils
from abautomator.exp_config import EXP_NAME, COND_ORDER
from abautomator.visualizer import RelDiffVisualizer

def render_specific_metrics(
        metric_list,
        metric_label,
        segments=["all", "android",  "ios", "new",  "existing"]
    ):

    layouts = _get_layouts(RelDiffVisualizer, metric_list, metric_label, segments)
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

def _get_layouts( vis_object, metric_list, metric_list_label, segments ):
    result = []
    for segment in segments:
        segment_layout = _get_segment_layout(segment, vis_object, metric_list, metric_list_label)
        result.append(segment_layout)
    return result

def _get_segment_layout(segment, vis_object, metric_list, metric_list_label):
    local_analy = pickle.load(
        open(os.path.join("..", "tests", "cache", f"{EXP_NAME}_analy_{segment}.p"), "rb" )
    )
    output_df = local_analy.get_rel_diff_confidence_intervals()
    df = utils.order_categories(output_df, metric_list, COND_ORDER)
    df = utils.remove_categories_w_no_order(df)
    source = utils.convert_df_to_source(df)

    vis = vis_object(source, title=f"{metric_list_label.title()} - {segment.title()}")
    return vis.get_layout()
