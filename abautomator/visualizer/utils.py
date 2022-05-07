from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, Span, Range1d, Label, Title
from bokeh.models import BoxZoomTool, ResetTool, PanTool, WheelZoomTool, SaveTool
import numpy as np
import logging

LOGGER = logging.getLogger()


def order_categories(df, metric_order, cond_order):
    metric_order_mapping = {item: i for i, item in enumerate(metric_order)}
    cond_order_mapping = {item: i for i, item in enumerate(cond_order)}

    df["metric_order"] = df['metric'].map(metric_order_mapping)
    df["cond_order"] = df['exp_cond'].map(cond_order_mapping)
    df = df.sort_values(by=['metric_order', 'cond_order'], ascending=(False, False))
    
    return df


def remove_categories_w_no_order(df):
    _check_for_nan_in_cols(df, ["metric_order", "cond_order"])
    return df.dropna(subset=['metric_order', 'cond_order'])

def _check_for_nan_in_cols(df, list_of_cols):
    for col in list_of_cols:
        _check_for_nan_in_col(df, col)

def _check_for_nan_in_col(df, col):
    nan_df = df[np.isnan(df[col])]
    if not nan_df.empty:
        LOGGER.warning(f"NaN values found!")

def remove_ungraphable_rows(df):
    _check_for_nan_in_cols(df, ["p_value", "std"])
    return df.dropna(subset=['p_value', 'std'])

def convert_df_to_source(df):
    df = df.copy()
    df = _transform_analyzed_df(df)
    return ColumnDataSource(df)


def _transform_analyzed_df(df):
    df["display_metric"] = df["metric"].str.replace("_", " ")
    df["display_metric"] = df["display_metric"].str.title()
    df["display_metric"] = df["display_metric"].str.replace("Pct", "%")
    df["factor_label"] = list(zip(df["display_metric"], df["exp_cond"]))
    return df


def get_metric_options(full_metric_list: np.ndarray):
    result = _get_ordered_metrics(full_metric_list)
    return _get_cleaned_metrics(result)


def _get_ordered_metrics(full_metric_list: np.ndarray):
    _, indexes = np.unique(full_metric_list, return_index=True)
    indexes.sort()
    return full_metric_list[indexes[::-1]]

def _get_cleaned_metrics(metric_list):
    return [
        item.replace("_", " ").title().replace("Pct", "%")
        for item in metric_list
    ]

def init_fig(cat_order, tool_tips):
    return figure(
        y_range=FactorRange(*cat_order),
        height=450,
        width=650,
        toolbar_location="right",
        tools=[BoxZoomTool(), WheelZoomTool(), PanTool(), ResetTool(), SaveTool()],
        tooltips=tool_tips,
    )

def add_zero_span(fig):
    zero_span = Span(
        location=0, dimension='height', line_color='grey', line_dash='dashed', line_alpha=0.8, line_width=1.5
    )
    fig.add_layout(zero_span)

def set_x_axis(fig, label, col_data_source):
    fig.xaxis.axis_label = label
    fig.xaxis.axis_label = label
    l_limit, r_limit = min(col_data_source.data["lower_95_ci"]), max(col_data_source.data["upper_95_ci"])
    span = r_limit - l_limit
    margin = span * 0.1
    fig.x_range = Range1d(
        min(0, l_limit) - margin,
        max(0, r_limit) + margin,
    )

def set_y_axis(fig):
    fig.yaxis.major_label_text_alpha = 0.0
    fig.yaxis.major_tick_in = 0
    fig.yaxis.major_tick_out = 0
    fig.yaxis.major_label_text_font_size = '1px'
    
    fig.yaxis.group_label_orientation = "horizontal"
    fig.yaxis.separator_line_alpha = 0
    fig.yaxis.minor_tick_line_color = "yellow"
    fig.ygrid.grid_line_color = None

def set_legend(fig):
    fig.legend.click_policy="mute"
    # fig.add_layout(fig.legend[0], 'right')

def set_fig_title(fig, title):
    if title:
        fig.add_layout(Title(text=title, align="center"), "above")
