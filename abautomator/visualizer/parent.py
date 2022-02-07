from bokeh.layouts import column

from abautomator.visualizer import core, sig, btn, utils, bars


class Visualizer:
    """ Parent object. Not to be initiated directly """

    def __init__(self, df, x_axis_label):
        self.df = df
        self.x_axis_label = x_axis_label

    def get_figure(self):
        source = utils.convert_df_to_source(self.df)

        fig = utils.init_fig(source, self._get_tool_tips())
        
        bars.add_core_bars(fig, source)

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
        source = utils.convert_df_to_source(self.df)

        fig = utils.init_fig(source, self._get_tool_tips())

        bars.add_core_bars(fig, source)
        bars.add_sig_bars(fig, source)

        self._setup_fig(fig)
        
        return column(fig, btn.get_stat_sig_btn(fig.renderers))

