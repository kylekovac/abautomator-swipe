import itertools

import numpy as np
from bokeh.models import CDSView, BooleanFilter
from bokeh.palettes import Colorblind8

from abautomator.visualizer import core, sig

def add_core_bars(fig, source):

    for cond_to_show, color in _cond_to_color_mapper(source).items():
        bools = [
            True if cond_to_show == exp_cond else False
            for exp_cond in source.data['exp_cond']
        ]
        view = CDSView(source=source, filters=[BooleanFilter(bools)])

        fig_core = (fig, source, view)

        lower_eb, upper_eb = add_error_bars(fig_core, core.get_error_bar)
        core_interval = core.add_interval(fig, cond_to_show, color, fig_core)

        core_interval.js_link('muted', lower_eb, 'muted')
        core_interval.js_link('muted', upper_eb, 'muted')


def _cond_to_color_mapper(source):
    colors = itertools.cycle(Colorblind8)
    return {exp_cond: color for exp_cond, color in zip(np.unique(source.data["exp_cond"]), colors)}


def add_error_bars(fig_core, _get_error_bar):
    upper_eb = _get_error_bar("upper_68_ci", "upper_95_ci", fig_core)
    lower_eb = _get_error_bar("lower_95_ci", "lower_68_ci", fig_core)
    
    return lower_eb, upper_eb


def add_sig_bars(fig, source):

    for exp_cond, color in _cond_to_color_mapper(source).items():
        bools = _get_bools_for_sig(source, exp_cond)
        view = CDSView(source=source, filters=[BooleanFilter(bools)])

        fig_core = (fig, source, view)

        lower_eb, upper_eb = add_error_bars(fig_core, sig.get_error_bar)
        sig_interval = sig.add_interval(fig, exp_cond, color, fig_core)

        sig_interval.js_link('visible', lower_eb, 'visible')
        sig_interval.js_link('visible', upper_eb, 'visible')
        sig_interval.visible = False
        lower_eb.visible = False
        upper_eb.visible = False
        sig_interval.tags = ["stat_sig"]


def _get_bools_for_sig(source, exp_cond):
    bools = []        
    for p_value, filter_cond in zip(source.data['p_value'], source.data['exp_cond']):
        if exp_cond == filter_cond and p_value <= 0.05:
            bools.append(True)
        else:
            bools.append(False)
    
    return bools
