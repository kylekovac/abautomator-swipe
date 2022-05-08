import os
import dill as pickle

from abautomator.visualizer import utils
from abautomator.exp_config import EXP_NAME, COND_ORDER

def _get_layouts(vis_object, metric_list, metric_list_label):
    result = []
    for mapping in [
                (None, "all"),
                ("device_type","android"),
                ("device_type", "ios"),
                ("user_type","new"),
                ("user_type", "existing"),
            ]:
        _, value = mapping
        local_analy = pickle.load(
            open(os.path.join("..", "notebooks", f"{EXP_NAME}_analy_{value}.p"), "rb" )
        )
        output_df = local_analy.get_rel_diff_confidence_intervals()
        df = utils.order_categories(output_df, metric_list, COND_ORDER)
        df = utils.remove_categories_w_no_order(df)
        source = utils.convert_df_to_source(df)

        vis = vis_object(source, title=f"{metric_list_label.title()} - {value.title()}")
        layout = vis.get_layout()
        result.append(layout)
    return result