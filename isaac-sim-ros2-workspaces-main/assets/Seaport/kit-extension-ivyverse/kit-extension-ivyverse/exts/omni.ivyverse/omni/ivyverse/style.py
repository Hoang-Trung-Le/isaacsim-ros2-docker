"""
Style configuration for Ivyverse UI
"""
# UI Colors
COLORS = {
    "primary": 0xFF00B4D8,
    "secondary": 0xFF0077B6,
    "accent": 0xFF90E0EF,
    "background": 0xFF1E1E1E,
    "surface": 0xFF2D2D2D,
    "text": 0xFFFFFFFF,
    "text_secondary": 0xFF909090,
    "error": 0xFFFF6B6B,
    "success": 0xFF4ECB71,
    "warning": 0xFFFFD93D
}
# UI Styles
WINDOW_STYLE = {
    "background_color": COLORS["background"],
    "border_color": COLORS["secondary"],
    "border_width": 1,
    "padding": 10
}
FRAME_STYLE = {
    "background_color": COLORS["surface"],
    "border_radius": 5,
    "padding": 8
}
BUTTON_STYLE = {
    "background_color": COLORS["primary"],
    "border_radius": 3,
    "padding": 5
}
BUTTON_HOVER_STYLE = {
    "background_color": COLORS["secondary"]
}
INPUT_STYLE = {
    "background_color": COLORS["surface"],
    "border_color": COLORS["primary"],
    "border_width": 1,
    "border_radius": 3,
    "padding": 5
}
LABEL_STYLE = {
    "color": COLORS["text"],
    "font_size": 14
}
HEADER_STYLE = {
    "color": COLORS["primary"],
    "font_size": 20,
    "font_weight": "bold"
}
# Chat message styles
USER_MESSAGE_STYLE = {
    "background_color": COLORS["surface"],
    "border_radius": 10,
    "padding": 10
}
ASSISTANT_MESSAGE_STYLE = {
    "background_color": COLORS["primary"],
    "border_radius": 10,
    "padding": 10
}
