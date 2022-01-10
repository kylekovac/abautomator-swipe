import itertools
import numpy as np

from bokeh.plotting import figure
from bokeh.models import CDSView, ColumnDataSource, FactorRange, BooleanFilter, Span
from bokeh.models import BoxZoomTool, ResetTool, PanTool
from bokeh.palettes import Colorblind8


def get_figure(df):
    source = ColumnDataSource(df)

    p = _init_figure(source)

    _add_zero_span(p)

    _add_bars(p, source)

    _set_legend(p)
    _set_x_axis(p)
    _set_y_axis(p)
    
    return p

def _init_figure(source: ColumnDataSource):
    return figure(
        y_range=FactorRange(*list(source.data["factor_label"])),
        height=450,
        title=f"exp name",
        toolbar_location="right",
        tools=[BoxZoomTool(), ResetTool(), PanTool()],
        tooltips= _get_tool_tips(),
    )

def _get_tool_tips():
    return [
        ("Rel Pop. Diff. x̄", "@{mean}±@{std}"),
        ("Abs Pop. Diff. x̄", "@{abs_mean}±@{abs_std}"),
        ("Tx x̄", "@{tx_mean}±@{tx_std}"),
        ("Ctrl x̄", "@{ctrl_mean}±@{ctrl_std}"),
        ("Tx Label", "@{exp_cond}"),
        ("Ctrl/Tx n", "@{ctrl_count}/@{tx_count}"),
    ]

def _add_zero_span(plot):
    zero_span = Span(
        location=0, dimension='height', line_color='grey', line_dash='dashed', line_alpha=0.8, line_width=1.5
    )
    plot.add_layout(zero_span)

def _add_bars(p, source):
    colors = itertools.cycle(Colorblind8)

    for exp_cond, color in zip(np.unique(source.data["exp_cond"]), colors):
        bools = [True if exp_cond == filter_cond else False for filter_cond in source.data['exp_cond']]
        view = CDSView(source=source, filters=[BooleanFilter(bools)])
        
        fig_core = (p, source, view)
        
        lower_eb, upper_eb = add_error_bars(fig_core)
        core_interval = add_core_interval(p, exp_cond, color, fig_core)

        core_interval.js_link('visible', lower_eb, 'visible')
        core_interval.js_link('visible', upper_eb, 'visible')

def add_error_bars(fig_core):
    upper_eb = _get_error_bar("upper_68_ci", "upper_95_ci", fig_core)
    lower_eb = _get_error_bar("lower_95_ci", "lower_68_ci", fig_core)
    
    return lower_eb, upper_eb
    
    
def _get_error_bar(left_label, right_label, fig_core):
    plot, source, view = fig_core
    return plot.segment(
        right_label,
        "factor_label",
        left_label,
        "factor_label",
        color="black",
        source=source,
        view=view,
    )

def add_core_interval(plot, exp_cond, color, fig_core):
    plot, source, view = fig_core
    return plot.hbar(
        y='factor_label',
        right="upper_68_ci",
        left="lower_68_ci",
        legend_label=exp_cond,
        fill_color=color,
        line_color=None,
        height=0.6,
        fill_alpha=0.8,
        source=source,
        view=view,
    )

def _set_legend(plot):
    plot.legend.location = "top_right"
    plot.legend.click_policy="hide"

def _set_x_axis(plot):
    plot.xaxis.axis_label = 'Relative difference from control (%)'

def _set_y_axis(plot):
    plot.yaxis.major_label_text_alpha = 0.0
    plot.yaxis.major_tick_in = 0
    plot.yaxis.major_tick_out = 0
    plot.yaxis.major_label_text_font_size = '1px'
    
    plot.yaxis.group_label_orientation = "horizontal"
    plot.yaxis.separator_line_alpha = 0
    plot.yaxis.minor_tick_line_color = "yellow"
    plot.ygrid.grid_line_color = None
