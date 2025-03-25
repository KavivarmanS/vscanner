# views/Theme.py
class Theme:
    def __init__(self, name, bg_color, fg_color, entry_bg, entry_fg, btn_bg, btn_fg, button_style, entry_style, header_bg, header_fg, gradient_start=None, gradient_end=None):
        self.name = name
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.entry_bg = entry_bg
        self.entry_fg = entry_fg
        self.btn_bg = btn_bg
        self.btn_fg = btn_fg
        self.button_style = button_style
        self.entry_style = entry_style
        self.header_bg = header_bg
        self.header_fg = header_fg
        self.gradient_start = gradient_start
        self.gradient_end = gradient_end

light_theme = Theme(
    name="light",
    bg_color="#ddf4f7",
    fg_color="#00796b",
    entry_bg="#ffffff",
    entry_fg="black",
    btn_bg="#4db6ac",
    btn_fg="#ffffff",
    button_style="Light.TButton",
    entry_style="Light.TEntry",
    header_bg="#b2ebf2",
    header_fg="#00796b",
    gradient_start="#e0f7fa",
    gradient_end="#4dd0e1"
)

dark_theme = Theme(
    name="dark",
    bg_color="#121212",
    fg_color="#ffffff",
    entry_bg="#333333",
    entry_fg="white",
    btn_bg="#333333",
    btn_fg="white",
    button_style="Dark.TButton",
    entry_style="Dark.TEntry",
    header_bg="#333333",
    header_fg="#ffffff",
    gradient_start="#121212",
    gradient_end="#444444"
)
