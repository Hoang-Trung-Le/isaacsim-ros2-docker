"""
Style configuration for Employee Management UI
Following Isaac Sim Omniverse extension styling standards
"""

import omni.ui as ui
from omni.ui import color as cl


class StyleSheet:
    """StyleSheet class following Isaac Sim Omniverse extension styling standards"""
    
    def __init__(self):
        self.default_attr = {"color": cl("#a1a1a1")}
        self.window_bg = {"background_color": cl("#2e2e2e")}
        
        # Define color scheme
        self.colors = {
            "primary": cl("#0078d4"),           # Blue - primary actions
            "secondary": cl("#6c757d"),         # Gray - secondary elements
            "success": cl("#28a745"),           # Green - success states
            "warning": cl("#ffc107"),           # Yellow - warnings
            "danger": cl("#dc3545"),            # Red - errors/alerts
            "info": cl("#17a2b8"),             # Cyan - info
            "light": cl("#f8f9fa"),            # Light gray
            "dark": cl("#343a40"),             # Dark gray
            "background": cl("#2e2e2e"),       # Main background
            "surface": cl("#3d3d3d"),          # Card/panel background
            "border": cl("#555555"),           # Border color
            "text_primary": cl("#ffffff"),      # Primary text
            "text_secondary": cl("#a1a1a1"),   # Secondary text
        }
        
        self.styles = {
            "window": {
                "background_color": self.colors["background"],
                "border_radius": 8,
                "padding": 10,
            },
            "collapsable_frame": {
                "background_color": self.colors["surface"],
                "border_radius": 6,
                "border_width": 1,
                "border_color": self.colors["border"],
                "padding": 8,
                "margin": 4,
            },
            "button": {
                "background_color": self.colors["primary"],
                "color": self.colors["text_primary"],
                "border_radius": 4,
                "padding": 8,
                "font_size": 14,
            },
            "button_secondary": {
                "background_color": self.colors["secondary"],
                "color": self.colors["text_primary"],
                "border_radius": 4,
                "padding": 8,
                "font_size": 14,
            },
            "button_success": {
                "background_color": self.colors["success"],
                "color": self.colors["text_primary"],
                "border_radius": 4,
                "padding": 8,
                "font_size": 14,
            },
            "button_warning": {
                "background_color": self.colors["warning"],
                "color": self.colors["dark"],
                "border_radius": 4,
                "padding": 8,
                "font_size": 14,
            },
            "button_danger": {
                "background_color": self.colors["danger"],
                "color": self.colors["text_primary"],
                "border_radius": 4,
                "padding": 8,
                "font_size": 14,
            },
            "label": {
                "color": self.colors["text_primary"],
                "font_size": 14,
                "margin": 2,
            },
            "label_secondary": {
                "color": self.colors["text_secondary"],
                "font_size": 12,
                "margin": 2,
            },
            "label_large": {
                "color": self.colors["text_primary"],
                "font_size": 16,
                # "font_weight": ui.FontWeight.BOLD,
                "margin": 4,
            },
            "text_field": {
                "background_color": self.colors["surface"],
                "color": self.colors["text_primary"],
                "border_radius": 4,
                "border_width": 1,
                "border_color": self.colors["border"],
                "padding": 6,
                "font_size": 14,
            },
            "combo_box": {
                "background_color": self.colors["surface"],
                "color": self.colors["text_primary"],
                "border_radius": 4,
                "border_width": 1,
                "border_color": self.colors["border"],
                "padding": 6,
                "font_size": 14,
            },
            "scrolling_frame": {
                "background_color": self.colors["surface"],
                "border_radius": 4,
                "border_width": 1,
                "border_color": self.colors["border"],
                "padding": 4,
            },
            "progress_bar": {
                "background_color": self.colors["surface"],
                "border_radius": 4,
                "height": 20,
            },
            "separator": {
                "color": self.colors["border"],
                "border_width": 1,
                "margin": 8,
            },
            "status_good": {
                "color": self.colors["success"],
                "font_size": 14,
                # "font_weight": ui.FontWeight.BOLD,
            },
            "status_warning": {
                "color": self.colors["warning"],
                "font_size": 14,
                # "font_weight": ui.FontWeight.BOLD,
            },
            "status_error": {
                "color": self.colors["danger"],
                "font_size": 14,
                # "font_weight": ui.FontWeight.BOLD,
            },
            "metric_value": {
                "color": self.colors["info"],
                "font_size": 18,
                # "font_weight": ui.FontWeight.BOLD,
                "alignment": ui.Alignment.CENTER,
            },
            "metric_label": {
                "color": self.colors["text_secondary"],
                "font_size": 12,
                "alignment": ui.Alignment.CENTER,
            },
        }


def get_style(style_sheet: StyleSheet, style_name: str) -> dict:
    """Get a specific style from the stylesheet"""
    if style_sheet and style_name in style_sheet.styles:
        return style_sheet.styles[style_name]
    return {}


# Global stylesheet instance
STYLESHEET_LOADED = True
try:
    default_stylesheet = StyleSheet()
except Exception as e:
    STYLESHEET_LOADED = False
    print(f"Warning: Could not load stylesheet: {e}")
    default_stylesheet = None
