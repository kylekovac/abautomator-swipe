import numpy as np
from bokeh.layouts import column, row

from abautomator.visualizer import widgets, utils, bars


class Visualizer:
    """ Parent object. Not to be initiated directly """

    def __init__(self, source, x_axis_label):
        self.source = source
        self.x_axis_label = x_axis_label

    def get_figure(self):
        fig = utils.init_fig(self._get_y_range(), self._get_tool_tips())
        
        bars.add_core_bars(fig, self.source)

        self._setup_fig(fig)
        
        return fig
    
    def _get_y_range(self):
        return list(self.source.data["factor_label"])
    
    def _setup_fig(self, fig):
        utils.add_zero_span(fig)
        utils.set_legend(fig)
        utils.set_x_axis(fig, self.x_axis_label)
        utils.set_y_axis(fig)
    
    def _get_tool_tips(self):
        pass  # To be implemented by children


class StatSigVisualizer(Visualizer):

    def get_figure(self):

        fig = utils.init_fig(self._get_y_range(), self._get_tool_tips())

        bars.add_core_bars(fig, self.source)
        bars.add_sig_bars(fig, self.source)

        self._setup_fig(fig)

        return fig
    
    def get_layout(self):

        fig = self.get_figure()

        metric_options = utils.get_metric_options(self.source.data["metric"])
        cond_options = list(np.unique(self.source.data["exp_cond"]))

        metric_widget, cond_widget = widgets.get_multichoice_widgets(
            fig.y_range, self.source, metric_options, cond_options
        )

        return row(
            fig,
            column(
                metric_widget,
                cond_widget,
                widgets.get_stat_sig_btn(fig.renderers),
                widgets.get_multichoice_reset_btn(metric_widget, cond_widget)
            ),
        )