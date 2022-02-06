import itertools
import numpy as np

from bokeh.plotting import figure
from bokeh.models import CDSView, ColumnDataSource, FactorRange, BooleanFilter, Span
from bokeh.models import BoxZoomTool, ResetTool, PanTool
from bokeh.palettes import Colorblind8


class Visualizer:
    """ Parent object. Not to be initiated directly """

    def __init__(self, df, x_axis_label):
        self.df = df
        self.x_axis_label = x_axis_label

    def get_figure(self):
        df = self.df.copy()
        df = _clean_exp_conds(df)
        source = ColumnDataSource(df)

        fig = _init_figure(source, self._get_tool_tips())

        _add_zero_span(fig)

        _add_bars(fig, source)

        # _set_legend(fig)
        _set_x_axis(fig, self.x_axis_label)
        _set_y_axis(fig)
        
        return fig
    
    def _get_tool_tips(self):
        pass  # To be implemented by children

def _clean_exp_conds(df):
    df["metric"] = df["metric"].str.replace("_", " ")
    df["metric"] = df["metric"].str.title()
    df["metric"] = df["metric"].str.replace("Pct", "%")
    df["factor_label"] = list(zip(df["metric"], df["exp_cond"]))
    return df

def _init_figure(source: ColumnDataSource, tool_tips):
    return figure(
        y_range=FactorRange(*list(source.data["factor_label"])),
        height=450,
        width=700,
        toolbar_location="right",
        tools=[BoxZoomTool(), ResetTool(), PanTool()],
        tooltips= tool_tips,
    )

def _add_zero_span(fig):
    zero_span = Span(
        location=0, dimension='height', line_color='grey', line_dash='dashed', line_alpha=0.8, line_width=1.5
    )
    fig.add_layout(zero_span)

def _add_bars(fig, source):
    colors = itertools.cycle(Colorblind8)

    for exp_cond, color in zip(np.unique(source.data["exp_cond"]), colors):
        bools = [
            True if exp_cond == filter_cond else False
            for filter_cond in source.data['exp_cond']
        ]
        view = CDSView(source=source, filters=[BooleanFilter(bools)])

        fig_core = (fig, source, view)

        lower_eb, upper_eb = add_error_bars(fig_core)
        core_interval = add_core_interval(fig, exp_cond, color, fig_core)

        core_interval.js_link('visible', lower_eb, 'visible')
        core_interval.js_link('visible', upper_eb, 'visible')

def add_error_bars(fig_core):
    upper_eb = _get_error_bar("upper_68_ci", "upper_95_ci", fig_core)
    lower_eb = _get_error_bar("lower_95_ci", "lower_68_ci", fig_core)
    
    return lower_eb, upper_eb
    
    
def _get_error_bar(left_label, right_label, fig_core):
    fig, source, view = fig_core
    return fig.segment(
        right_label,
        "factor_label",
        left_label,
        "factor_label",
        color="black",
        source=source,
        view=view,
    )

def add_core_interval(fig, exp_cond, color, fig_core):
    fig, source, view = fig_core
    return fig.hbar(
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

def _set_legend(fig):
    fig.legend.click_policy="hide"
    fig.add_layout(fig.legend[0], 'right')

def _set_x_axis(fig, label):
    fig.xaxis.axis_label = label
    # 'Relative difference from control (%)'

def _set_y_axis(fig):
    fig.yaxis.major_label_text_alpha = 0.0
    fig.yaxis.major_tick_in = 0
    fig.yaxis.major_tick_out = 0
    fig.yaxis.major_label_text_font_size = '1px'
    
    fig.yaxis.group_label_orientation = "horizontal"
    fig.yaxis.separator_line_alpha = 0
    fig.yaxis.minor_tick_line_color = "yellow"
    fig.ygrid.grid_line_color = None
