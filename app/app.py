from flask import Flask, redirect, url_for


from abautomator.exp_config import PRIMARY_METRIC_LIST, SECONDARY_METRIC_LIST, GUARDRAIL_METRIC_LIST
from app import utils

app = Flask(__name__)

@app.route('/<metric_set>/')
@app.route('/<metric_set>/<segment>')
def get_graphs(metric_set="primary", segment=None):
    if not segment:
        return redirect(url_for("get_graphs", metric_set=metric_set, segment='all-charts'))
    metric_mapping = {
        'primary': PRIMARY_METRIC_LIST,
        'secondary': SECONDARY_METRIC_LIST,
        'guardrail': GUARDRAIL_METRIC_LIST,
    }
    if segment == "all-charts":
        return utils.render_specific_metrics(metric_mapping[metric_set], f"{metric_set} metrics")
    else:
        return utils.render_specific_metrics(metric_mapping[metric_set], f"{metric_set} metrics", [segment])
