"""
Style definitions for OmniAlert Extension
Provides styling constants and methods for UI components
"""

from typing import Dict, Any
from .alert_types import AlertSeverity


class OmniAlertStyle:
    """Style constants and methods for OmniAlert UI"""

    # Color constants
    COLORS = {
        # Alert severity colors
        "critical": 0xFFFF4444,  # Red
        "high": 0xFFFF8800,      # Orange
        "medium": 0xFFFFDD00,    # Yellow
        "low": 0xFF44AAFF,       # Blue
        "info": 0xFF888888,      # Gray
        
        # UI colors
        "background": 0xFF2A2A2A,
        "background_alt": 0xFF3A3A3A,
        "text_primary": 0xFFFFFFFF,
        "text_secondary": 0xFFCCCCCC,
        "text_muted": 0xFF888888,
        "border": 0xFF555555,
        "accent": 0xFF2E5D8E,
        "success": 0xFF2E8E5D,
        "warning": 0xFFE6A532,
        "error": 0xFFD32F2F,
    }

    # Text styles
    TEXT_STYLES = {
        "title": {
            "font_size": 18,
            "color": COLORS["text_primary"],
            "alignment": "left"
        },
        "heading": {
            "font_size": 16,
            "color": COLORS["text_primary"],
            "alignment": "left"
        },
        "subheading": {
            "font_size": 14,
            "color": COLORS["text_secondary"],
            "alignment": "left"
        },
        "body": {
            "font_size": 12,
            "color": COLORS["text_primary"],
            "alignment": "left"
        },
        "caption": {
            "font_size": 10,
            "color": COLORS["text_muted"],
            "alignment": "left"
        }
    }

    # Button styles
    BUTTON_STYLES = {
        "primary": {
            "background_color": COLORS["accent"],
            "color": COLORS["text_primary"],
            "border_radius": 4,
            "padding": 8
        },
        "secondary": {
            "background_color": COLORS["background_alt"],
            "color": COLORS["text_secondary"],
            "border_radius": 4,
            "padding": 8
        },
        "success": {
            "background_color": COLORS["success"],
            "color": COLORS["text_primary"],
            "border_radius": 4,
            "padding": 8
        },
        "warning": {
            "background_color": COLORS["warning"],
            "color": COLORS["text_primary"],
            "border_radius": 4,
            "padding": 8
        },
        "error": {
            "background_color": COLORS["error"],
            "color": COLORS["text_primary"],
            "border_radius": 4,
            "padding": 8
        },
        "tab": {
            "background_color": COLORS["background_alt"],
            "color": COLORS["text_secondary"],
            "border_radius": 4,
            "padding": 6
        }
    }

    @classmethod
    def get_alert_color(cls, severity: AlertSeverity) -> int:
        """Get color for alert severity"""
        severity_colors = {
            AlertSeverity.CRITICAL: cls.COLORS["critical"],
            AlertSeverity.HIGH: cls.COLORS["high"],
            AlertSeverity.MEDIUM: cls.COLORS["medium"],
            AlertSeverity.LOW: cls.COLORS["low"],
            AlertSeverity.INFO: cls.COLORS["info"],
        }
        return severity_colors.get(severity, cls.COLORS["info"])

    @classmethod
    def get_text_style(cls, style_name: str) -> Dict[str, Any]:
        """Get text style by name"""
        return cls.TEXT_STYLES.get(style_name, cls.TEXT_STYLES["body"]).copy()

    @classmethod
    def get_button_style(cls, style_name: str) -> Dict[str, Any]:
        """Get button style by name"""
        return cls.BUTTON_STYLES.get(style_name, cls.BUTTON_STYLES["primary"]).copy()

    @classmethod
    def get_severity_icon(cls, severity: AlertSeverity) -> str:
        """Get icon for alert severity"""
        icons = {
            AlertSeverity.CRITICAL: "🚨",
            AlertSeverity.HIGH: "⚠️",
            AlertSeverity.MEDIUM: "📢",
            AlertSeverity.LOW: "ℹ️",
            AlertSeverity.INFO: "💬",
        }
        return icons.get(severity, "❓")

    @classmethod
    def get_category_icon(cls, category_name: str) -> str:
        """Get icon for alert category"""
        icons = {
            "safety": "🛡️",
            "equipment": "⚙️",
            "process": "🔄",
            "environmental": "🌡️",
            "employee": "👤",
            "inventory": "📦",
            "quality": "✅",
            "security": "🔒",
            "maintenance": "🔧",
            "system": "💻",
        }
        return icons.get(category_name.lower(), "📋")

    @classmethod
    def get_industrial_theme(cls) -> Dict[str, Any]:
        """Get complete industrial theme configuration"""
        return {
            "colors": cls.COLORS.copy(),
            "text_styles": cls.TEXT_STYLES.copy(),
            "button_styles": cls.BUTTON_STYLES.copy(),
            "spacing": {
                "small": 4,
                "medium": 8,
                "large": 16,
                "xlarge": 24
            },
            "borders": {
                "width": 1,
                "radius": 4,
                "color": cls.COLORS["border"]
            }
        } 