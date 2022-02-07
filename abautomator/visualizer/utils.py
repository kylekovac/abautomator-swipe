from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, Span
from bokeh.models import BoxZoomTool, ResetTool, PanTool


def convert_df_to_source(df):
    df = df.copy()
    df = _clean_analyzed_df(df)
    return ColumnDataSource(df)


def _clean_analyzed_df(df):
    df["metric"] = df["metric"].str.replace("_", " ")
    df["metric"] = df["metric"].str.title()
    df["metric"] = df["metric"].str.replace("Pct", "%")
    df["factor_label"] = list(zip(df["metric"], df["exp_cond"]))
    return df

def init_fig(source: ColumnDataSource, tool_tips):
    return figure(
        y_range=FactorRange(*list(source.data["factor_label"])),
        height=450,
        width=700,
        toolbar_location="right",
        tools=[BoxZoomTool(), ResetTool(), PanTool()],
        tooltips= tool_tips,
    )

def add_zero_span(fig):
    zero_span = Span(
        location=0, dimension='height', line_color='grey', line_dash='dashed', line_alpha=0.8, line_width=1.5
    )
    fig.add_layout(zero_span)

def set_x_axis(fig, label):
    fig.xaxis.axis_label = label

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
    fig.add_layout(fig.legend[0], 'right')