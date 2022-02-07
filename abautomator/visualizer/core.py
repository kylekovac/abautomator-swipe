""" Functions for drawing "core" data on figure

(all data w/o regard to significance)
"""

def add_interval(fig, exp_cond, color, fig_core):
    fig, source, view = fig_core
    renderer = fig.hbar(
        y='factor_label',
        right="upper_68_ci",
        left="lower_68_ci",
        legend_label=exp_cond,
        fill_color=color,
        line_color=None,
        fill_alpha=0.8,
        muted_color=color,
        muted_alpha=0.2,
        height=0.6,
        source=source,
        view=view,
    )
    return renderer

def get_error_bar(left_label, right_label, fig_core):
    fig, source, view = fig_core
    return fig.segment(
        right_label,
        "factor_label",
        left_label,
        "factor_label",
        color="black",
        muted_color="black",
        muted_alpha=0.2,
        source=source,
        view=view,
    )