from bokeh.layouts import column

from abautomator.visualizer import core, sig, btn, utils, bars


class Visualizer:
    """ Parent object. Not to be initiated directly """

    def __init__(self, cat_order, x_axis_label, source):
        self.cat_order = cat_order
        self.source = source
        self.x_axis_label = x_axis_label

    def get_figure(self):
        fig = utils.init_fig(self.cat_order, self._get_tool_tips())
        
        bars.add_core_bars(fig, self.source)

        self._setup_fig(fig)
        
        return fig
    
    def _setup_fig(self, fig):
        utils.add_zero_span(fig)
        utils.set_legend(fig)
        utils.set_x_axis(fig, self.x_axis_label)
        utils.set_y_axis(fig)
    
    def _get_tool_tips(self):
        pass  # To be implemented by children


class StatSigVisualizer(Visualizer):

    def get_figure(self):

        fig = utils.init_fig(self.cat_order, self._get_tool_tips())

        bars.add_core_bars(fig, self.source)
        bars.add_sig_bars(fig, self.source)

        self._setup_fig(fig)

        return fig
    
    def get_layout(fig):
        
        return column(fig, btn.get_stat_sig_btn(fig.renderers))

