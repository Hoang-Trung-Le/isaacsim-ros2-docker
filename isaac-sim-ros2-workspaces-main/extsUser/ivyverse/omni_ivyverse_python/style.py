"""
Style configuration for Ivyverse UI following Omniverse extension standards
"""

import carb.tokens
import omni.ui as ui
import omni.ui.color_utils as cl
import omni.ui.constant_utils as ct

# Resolve paths for assets (standard Omniverse practice)
icon_path = carb.tokens.get_tokens_interface().resolve("${ivyverse}/icons")
print(f"ivyverse icon_path: {icon_path}")


# Define base colors following standard pattern
cl.primary_color = cl.color("#00B4D8")
cl.secondary_color = cl.color("#0077B6")
cl.accent_color = cl.color("#90E0EF")
cl.background_color = cl.color("#1E1E1E")
cl.surface_color = cl.color("#2D2D2D")
cl.color.white = cl.color("#FFFFFF")
cl.black_color = cl.color("#000000")
cl.text_secondary_color = cl.color("#909090")
cl.error_color = cl.color("#FF6B6B")
cl.success_color = cl.color("#4ECB71")
cl.warning_color = cl.color("#FFD93D")
cl.separator_color = cl.color("#FFFFFF33")
cl.panel_bg_color = cl.color("#2A2A2A")
cl.border_color = cl.color("#3A3A3A")
cl.highlight_color = cl.color("#90E0EFAA")
cl.disabled_color = cl.color("#666666")
cl.input_field_bg_color = cl.color("#121212")
cl.button_bg_color = cl.color("#181818")
cl.button_bg_border_color = cl.color("#696969")


# Font sizes following standard pattern
ct.font_size_xlarge = 24
ct.font_size_large = 20
ct.font_size_medium = 16
ct.font_size_normal = 14
ct.font_size_small = 12
ct.font_size_tiny = 10


# Main comprehensive style dictionary following standard Omniverse pattern
ivyverse_style = {
    # Window styling
    "Window": {
        "background_color": cl.background_color,
        "border_color": cl.secondary_color,
        "border_width": 1,
        "border_radius": 5,
        "padding": 12,
    },
    # Frame styling
    "Frame": {
        "background_color": cl.surface_color,
        "border_radius": 5,
        "padding": 8,
    },
    "Frame::main": {
        "background_color": cl.background_color,
        "border_color": cl.border_color,
        "border_width": 1,
        "border_radius": 8,
        "padding": 12,
    },
    "Frame::panel": {
        "background_color": cl.panel_bg_color,
        "border_radius": 5,
        "margin": 4,
        "padding": 8,
    },
    # Button styling with standard selectors
    "Button": {
        "background_color": cl.primary_color,
        "border_radius": 3,
        "border_width": 1,
        "border_color": cl.color("#FFFFFF33"),
        "padding": 8,
    },
    "Button.Label": {
        "color": cl.color.white,
        "font_size": ct.font_size_normal,
    },
    "Button:hovered": {
        "background_color": cl.secondary_color,
        "border_color": cl.color("#FFFFFF66"),
    },
    "Button:pressed": {
        "background_color": cl.accent_color,
    },
    "Button::primary": {
        "background_color": cl.primary_color,
    },
    "Button::secondary": {
        "background_color": cl.surface_color,
        "border_color": cl.border_color,
    },
    "Button::send": {
        "background_color": cl.primary_color,
        # "border_radius": 20,
    },
    "Button.Image::send": {
        "color": cl.color.white,
        "image_url": f"{icon_path}/submitButton.svg" if icon_path else None,
    },
    "Button.Image::send:hovered": {
        "color": cl.accent_color,
    },
    "Button.Image::voice": {
        "image_url": f"{icon_path}/voice.svg",
        "color": cl.color.white,
    },
    "Button.Image::audio-wave": {
        "image_url": f"{icon_path}/audio-wave.svg",
        "color": cl.color.white,
    },
    "Button.Image::stop": {
        "image_url": f"{icon_path}/stop-button.svg",
        "color": cl.color.white,
    },
    "Button.Image::conversation": {
        "image_url": f"{icon_path}/conversation-bubble-chat.svg",
        "color": cl.color.white,
    },
    "Button.Image::upload": {
        "image_url": f"{icon_path}/uploadButton.svg",
        "color": cl.color.white,
    },
    "Button.Image::upload:hovered": {
        "color": cl.accent_color,
    },
    "Button.Image::upload:pressed": {
        "color": cl.accent_color,
    },
    "StringField": {
        "background_color": cl.color.black,
        "color": cl.color.white,
        "border_color": cl.border_color,
        "border_radius": 4,
        "padding": 8,
    },
    "StringField::api-key-field": {
        "background_color": cl.primary_color,
        "color": cl.color.white,
        "border_color": cl.border_color,
        "border_radius": 4,
        "padding": 8,
    },
    "StringField::chat-input": {
        "background_color": cl.color.black,
        "color": cl.color.white,
        "border_color": cl.border_color,
        "border_radius": 4,
        "padding": 8,
    },
    # InputField styling (for StringFields with style_type_name_override)
    "InputField": {
        "background_color": cl.input_field_bg_color,
        "color": cl.color.white,
        "border_color": cl.border_color,
        "border_width": 1,
        "border_radius": 4,
        "padding": 8,
        "font_size": ct.font_size_normal,
    },
    "InputField::api-key-field": {
        "background_color": cl.color.black,
        "color": cl.color.white,
        "border_color": cl.accent_color,
        "border_width": 1,
        "border_radius": 4,
        "padding": 8,
        "font_size": ct.font_size_normal,
    },
    "InputField::chat-input": {
        "background_color": cl.color.black,
        "color": cl.color.white,
        "border_color": cl.primary_color,
        "border_width": 1,
        "border_radius": 4,
        "padding": 8,
        "font_size": ct.font_size_normal,
    },
    # ComboBox styling
    "ComboBox": {
        "color": cl.color.white,
        "background_color": cl.surface_color,
        "secondary_color": cl.panel_bg_color,
        "selected_color": cl.primary_color,
        "secondary_selected_color": cl.color.white,
        "border_color": cl.primary_color,
        "border_width": 1,
        "border_radius": 4,
        "font_size": ct.font_size_normal,
        "padding": 5,
    },
    "ComboBox:focused": {
        "border_color": cl.accent_color,
    },
    "ComboBox:disabled": {
        "background_color": cl.disabled_color,
        "border_color": cl.border_color,
    },
    # Label styling with variants
    "Label": {
        "color": cl.color.white,
        "font_size": ct.font_size_normal,
    },
    "Label::header": {
        "color": cl.primary_color,
        "font_size": ct.font_size_large,
    },
    "Label::header-main": {
        "color": cl.primary_color,
        "font_size": ct.font_size_xlarge,
    },
    "Label::header-sub": {
        "color": cl.color.white,
        "font_size": ct.font_size_normal,
    },
    "Label::header-chat": {
        "color": cl.color.white,
        "font_size": ct.font_size_large,
    },
    "Label::secondary": {
        "color": cl.text_secondary_color,
        "font_size": ct.font_size_normal,
    },
    "Label::chat-user": {
        "color": cl.color.white,
        "font_size": ct.font_size_medium,
    },
    "Label::chat-assistant": {
        "color": cl.color.white,
        "font_size": ct.font_size_medium,
    },
    "Label::error": {
        "color": cl.error_color,
    },
    "Label::success": {
        "color": cl.success_color,
    },
    "Label::warning": {
        "color": cl.warning_color,
    },
    # Rectangle styling for chat messages and containers
    "Rectangle": {
        "background_color": cl.surface_color,
        "border_radius": 8,
    },
    "Rectangle::user-message": {
        "background_color": cl.surface_color,
        "border_radius": 8,
        "padding": 8,
    },
    "Rectangle::assistant-message": {
        "background_color": cl.primary_color,
        "border_radius": 8,
        "padding": 8,
    },
    "Rectangle::panel": {
        "background_color": cl.panel_bg_color,
        "border_radius": 5,
        "border_width": 1,
        "border_color": cl.border_color,
    },
    "Rectangle::highlight": {
        "background_color": cl.highlight_color,
    },
    # CollapsableFrame styling
    "CollapsableFrame": {
        "background_color": cl.panel_bg_color,
        "secondary_color": cl.color.transparent,
        "border_radius": 5,
        "margin_height": 4,
        "border_width": 0,
        "font_size": ct.font_size_normal,
    },
    "CollapsableFrame:hovered": {
        "background_color": cl.color("#333333"),
    },
    "CollapsableFrame::main": {
        "background_color": cl.surface_color,
        "border_color": cl.border_color,
        "border_width": 1,
    },
    # Line/Separator styling
    "Line": {
        "color": cl.separator_color,
        "border_width": 1,
    },
    "Separator": {
        "color": cl.separator_color,
        "margin_height": 12,
    },
    # ScrollingFrame styling
    "ScrollingFrame": {
        "background_color": cl.color.transparent,
        "secondary_color": cl.color.gray,
        "scrollbar_size": 4,
    },
    "ScrollingFrame::chat-history": {
        "background_color": cl.color.black,
        "scrollbar_size": 6,
        # "debug_color": cl.color.red,
    },
    # TreeView styling
    "TreeView": {
        "background_color": cl.color.transparent,
        "background_selected_color": cl.color.transparent,
    },
    "TreeView:selected": {
        "background_color": cl.highlight_color,
    },
    "TreeView::chat": {
        "background_selected_color": ui.color.transparent,
    },
    "TreeView::chat:selected": {
        "background_color": ui.color.transparent,
    },
    # Image styling
    "Image::user-avatar": {
        "border_radius": 20,
        "image_url": f"{icon_path}/user-avatar.png" if icon_path else None,
    },
    "Image::assistant-avatar": {
        "border_radius": 20,
        "image_url": f"{icon_path}/assistant-avatar.png" if icon_path else None,
    },
    "Image::ivyverse-logo": {
        "image_url": f"{icon_path}/ivyverse1.svg",
        # "border_width": 1,
        # "border_color": cl("#1ab3ff"),
        # "border_radius": 1,
        "fill_policy": ui.FillPolicy.PRESERVE_ASPECT_FIT,
        "alignment": ui.Alignment.CENTER,
    },
}


# Backward compatibility - individual style dictionaries (keeping the modular approach)
# class StyleComponents:
#     """Individual style components for backward compatibility and modular usage"""

#     window = {"Window": ivyverse_style["Window"]}

#     frame = {"Frame": ivyverse_style["Frame"]}

#     button = {
#         "Button": ivyverse_style["Button"],
#         "Button.Label": ivyverse_style["Button.Label"],
#         "Button:hovered": ivyverse_style["Button:hovered"],
#         "Button:pressed": ivyverse_style["Button:pressed"],
#     }

#     input_field = {
#         "TextField": ivyverse_style["TextField"],
#         "TextField:focused": ivyverse_style["TextField:focused"],
#         "TextField:disabled": ivyverse_style["TextField:disabled"],
#     }

#     combo_box = {
#         "ComboBox": ivyverse_style["ComboBox"],
#         "ComboBox:focused": ivyverse_style["ComboBox:focused"],
#         "ComboBox:disabled": ivyverse_style["ComboBox:disabled"],
#     }

#     label = {"Label": ivyverse_style["Label"]}

#     header = {"Label": ivyverse_style["Label::header"]}

#     user_message = {"Rectangle": ivyverse_style["Rectangle::user-message"]}

#     assistant_message = {"Rectangle": ivyverse_style["Rectangle::assistant-message"]}

#     separator = {"Separator": ivyverse_style["Separator"]}

#     collapsable_frame = {
#         "CollapsableFrame": ivyverse_style["CollapsableFrame"],
#         "CollapsableFrame:hovered": ivyverse_style["CollapsableFrame:hovered"],
#     }


# # Update StyleSheet class with legacy compatibility
# class StyleSheet:
#     """StyleSheet class following Isaac Sim Omniverse extension styling standards"""

#     # --- Constants and Configuration (keeping the good organizational approach) ---

#     # Color dictionary for easy reference and updates
#     COLORS = {
#         "primary": cl.primary_color,
#         "secondary": cl.secondary_color,
#         "accent": cl.accent_color,
#         "background": cl.background_color,
#         "surface": cl.surface_color,
#         "text_white": cl.color.white,
#         "text_secondary": cl.text_secondary_color,
#         "error": cl.error_color,
#         "success": cl.success_color,
#         "warning": cl.warning_color,
#         "separator": cl.separator_color,
#         "panel_bg": cl.panel_bg_color,
#         "border": cl.border_color,
#         "highlight": cl.highlight_color,
#         "disabled": cl.disabled_color,
#         "black": cl.color("#000000"),
#         "white": cl.color("#FFFFFF"),
#     }

#     # Font size dictionary for consistency
#     FONT_SIZES = {
#         "xlarge": ct.font_size_xlarge,
#         "large": ct.font_size_large,
#         "medium": ct.font_size_medium,
#         "normal": ct.font_size_normal,
#         "small": ct.font_size_small,
#         "tiny": ct.font_size_tiny,
#     }

#     # Spacing and layout constants
#     SPACING = {
#         "tiny": 2,
#         "small": 4,
#         "medium": 8,
#         "large": 12,
#         "xlarge": 16,
#     }

#     # Border radius for different components
#     BORDER_RADIUS = {
#         "small": 3,
#         "medium": 5,
#         "large": 8,
#         "round": 20,
#     }

#     # Legacy compatibility properties
#     window = StyleComponents.window
#     frame = StyleComponents.frame
#     button = StyleComponents.button
#     input_field = StyleComponents.input_field
#     dropdown = StyleComponents.combo_box
#     combo_box = StyleComponents.combo_box
#     label = StyleComponents.label
#     header = StyleComponents.header
#     user_message = StyleComponents.user_message
#     assistant_message = StyleComponents.assistant_message
#     separator = StyleComponents.separator
#     collapsable_frame = StyleComponents.collapsable_frame

#     # Additional legacy properties
#     chat_history = {
#         "background_color": cl.color.black,
#         "padding": 10,
#         # "debug_color": cl.color.blue,
#     }

#     chat_input = {
#         "background_color": cl.color("#000000"),
#         "border_color": cl.border_color,
#         "border_width": 1,
#         "border_radius": 4,
#         "color": cl.color.white,
#         "padding": 8,
#     }
