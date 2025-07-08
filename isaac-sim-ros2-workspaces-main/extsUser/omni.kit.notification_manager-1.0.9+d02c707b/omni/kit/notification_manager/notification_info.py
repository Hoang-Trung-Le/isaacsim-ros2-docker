__all__ = ["NotificationButtonInfo", "NotificationStatus"]

from typing import Callable

class NotificationStatus:
    """
    Notification status.

    Different status has different icon and background color.

    Could be:
        - NotificationStatus.INFO
        - NotificationStatus.WARNING
    """

    
    WARNING = 0
    """
    Warning Notification.
    """

    INFO = 1
    """
    Information Notification.
    """
    


class NotificationButtonInfo:
    
    """
    Represent a button in notification.

    Args:
        text (str): The button text.

    Keyword Args:
        on_complete (Callable[[None], None]): The button handler when clicked.
    """
    def __init__(self, text, on_complete: Callable[[None], None] = None):
        self._text = text
        self._on_complete = on_complete
    
    @property
    def text(self):
        """Button text"""
        return self._text

    @property
    def handler(self):
        """Button handler when clicked"""
        return self._on_complete


class NotificationInfo:
    def __init__(
        self,
        text,
        hide_after_timeout=True,
        duration=3,
        status=NotificationStatus.INFO,
        button_infos=[]):
        self._text = text
        self._hide_after_timeout = hide_after_timeout
        self._duration = duration
        self._status = status
        if not button_infos and not hide_after_timeout:
            button_info = NotificationButtonInfo("Dismiss", None)
            self._button_infos = [button_info]
        else:
            self._button_infos = button_infos
    
    @property
    def text(self):
        return self._text
    
    @property
    def hide_after_timeout(self):
        return self._hide_after_timeout

    @property
    def duration(self):
        return self._duration

    @property
    def status(self):
        return self._status

    @property
    def button_infos(self):
        return self._button_infos
