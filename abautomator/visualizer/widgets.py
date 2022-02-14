from bokeh.models import Toggle, CustomJS, MultiChoice, Button


def get_multichoice_widgets(y_range, source, metric_options, cond_options):
    metric_widget = MultiChoice(value=metric_options, options=metric_options)
    cond_widget = MultiChoice(value=cond_options, options=cond_options)
    
    callback = CustomJS(
        args=dict(
            yRange=y_range,
            source=source,
            metricWidget=metric_widget,
            condWidget=cond_widget,
        ),
        code="""
        // Filter y-axis labels
        let tempList = source.data["factor_label"].filter(function (currentElement) {
          return metricWidget.value.includes(currentElement[0]) && condWidget.value.includes(currentElement[1]);
        });
        yRange.factors = tempList;
        """
    )
    metric_widget.js_on_change("value", callback)
    cond_widget.js_on_change("value", callback)
    return metric_widget, cond_widget


def get_multichoice_reset_btn(metric_widget, cond_widget):
    button = Button(label="Rest Metrics/Conditions", button_type="success")
    callback = CustomJS(
        args=dict(metricWidget=metric_widget, condWidget=cond_widget),
        code="""
        metricWidget.value = metricWidget.options
        condWidget.value = condWidget.options
        """
    )
    button.js_on_click(callback)
    return button


def get_stat_sig_btn(renderers):
    button = Toggle(label="Toggle Stat Sig", button_type="danger")
    callback = CustomJS(
        args=dict(glyphs=renderers),
        code="""
        for (const glyph of glyphs){
            if (glyph.tags.includes("stat_sig")) {
                var stat_sig_visible = glyph.visible;
            }
        }

        if (stat_sig_visible) {
            var muted = false;
        } else {
            var muted = true;
        }

        for (const glyph of glyphs){
            if (glyph.tags.includes("stat_sig")) {
                glyph.visible = !glyph.visible;
            } else {
                glyph.muted = muted;
            }
        }
        """
        )

    button.js_on_click(callback)

    return button
