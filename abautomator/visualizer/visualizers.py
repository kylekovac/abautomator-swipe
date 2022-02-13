from .parent import Visualizer, StatSigVisualizer

class BasicVisualizer(Visualizer):

    def __init__(self, cat_order, source):
        super().__init__(cat_order, "Population Mean/Proportion (x̄/p̂)", source)
    
    def _get_tool_tips(self):
        return [
            ("x̄", "@{mean}±@{std}"),
            ("N", "@{count}"),
        ]

class AbsDiffVisualizer(StatSigVisualizer):

    def __init__(self, cat_order, source):
        super().__init__(cat_order, "Tx - Ctrl Population (Absolute Diff.)", source)
    
    def _get_tool_tips(self):
        return [
            ("Tx Label", "@{exp_cond}"),
            ("Tx x̄ - Ctrl x̄", "@{mean}±@{std}"),
            ("P-Value", "@p_value{1.11111}"),  # https://stackoverflow.com/questions/28999411/how-to-show-integer-not-float-with-hover-tooltip-in-bokeh
            ("Ctrl x̄", "@{ctrl_mean}±@{ctrl_std}"),
            ("Tx x̄", "@{tx_mean}±@{tx_std}"),
            ("Ctrl/Tx n", "@{ctrl_count}/@{tx_count}"),
        ]

class RelDiffVisualizer(StatSigVisualizer):

    def __init__(self, cat_order, source):
        super().__init__(cat_order, "Relative Diff. of Tx Pop vs Ctrl Pop (%)", source)
    
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
