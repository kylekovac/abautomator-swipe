from bokeh.models import Button, CustomJS

def get_stat_sig_btn(renderers):
    button = Button(label="Toggle Stat Sig", button_type="danger")
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
