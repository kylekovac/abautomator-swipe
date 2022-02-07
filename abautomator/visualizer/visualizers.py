from .parent import Visualizer

class BasicVisualizer(Visualizer):

    def __init__(self, df):
        super().__init__(df, "Population Mean/Proportion (x̄/p̂)")
    
    def _get_tool_tips(self):
        return [
            ("x̄", "@{mean}±@{std}"),
            ("N", "@{count}"),
        ]

class AbsDiffVisualizer(Visualizer):

    def __init__(self, df):
        super().__init__(df, "Tx - Ctrl Population (Absolute Diff.)")
    
    def _get_tool_tips(self):
        return [
            ("Tx Label", "@{exp_cond}"),
            ("Tx x̄ - Ctrl x̄", "@{mean}±@{std}"),
            ("P-Value", "@p_value{1.11111}"),  # https://stackoverflow.com/questions/28999411/how-to-show-integer-not-float-with-hover-tooltip-in-bokeh
            ("Ctrl x̄", "@{ctrl_mean}±@{ctrl_std}"),
            ("Tx x̄", "@{tx_mean}±@{tx_std}"),
            ("Ctrl/Tx n", "@{ctrl_count}/@{tx_count}"),
        ]

class RelDiffVisualizer(Visualizer):

    def __init__(self, df):
        super().__init__(df, "Relative Diff. of Tx Pop vs Ctrl Pop (%)")
    
    def _get_tool_tips(self):
        return [
            ("Tx Label", "@{exp_cond}"),
            ("Rel Diff Tx vs Ctrl", "@{mean}±@{std}"),
            ("P-Value", "@p_value{1.11111}"),  # https://stackoverflow.com/questions/28999411/how-to-show-integer-not-float-with-hover-tooltip-in-bokeh
            ("Abs Diff Tx - Ctrl", "@{abs_mean}±@{abs_std}"),
            ("Ctrl x̄", "@{ctrl_mean}±@{ctrl_std}"),
            ("Tx x̄", "@{tx_mean}±@{tx_std}"),
            ("Ctrl/Tx n", "@{ctrl_count}/@{tx_count}"),
        ]
