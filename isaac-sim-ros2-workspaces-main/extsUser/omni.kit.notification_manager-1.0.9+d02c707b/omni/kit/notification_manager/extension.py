# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["post_notification", "destroy_all_notifications", "get_all_notifications", "NotificationManagerExtension"]

import weakref

import omni.ext

from .manager import NotificationManager
from .notification_info import NotificationInfo, NotificationStatus


_global_instance = None


def post_notification(
    text,
    hide_after_timeout=True,
    duration=3,
    status=NotificationStatus.INFO,
    button_infos=[],
):
    """
    Post notification.
    If viewport is visible, it will be docked to the right-bottom of viewport.
    Otherwise, it will be docked to main window.

    Args:
        text (str): The notification text.

    Keyword Args:
        hide_after_timeout (bool): If the notification will hide after duration.
                                    If it's False, and button_details are not provided, it will display a default dismiss button.
        duration (int): The duration (in seconds) after which the notification will be hidden.
                        This duration only works if hide_after_timeout is True.
        status (NotificationStatus): The notification type. By default, NotificationStatus.INFO as information.
        button_infos ([NotificationButtonInfo]): Array of buttons.

    Returns:
        Notification handler.
    
    Examples:

        >>> import omni.kit.notification_manager as nm
        >>> ok_button = nm.NotificationButtonInfo("OK", on_complete=None)
        >>> cancel_button = nm.NotificationButtonInfo("CANCEL", on_complete=None)
        >>> notification = nm.post_notification(
                    "Notification Example",
                    hide_after_timeout=False,
                    duration=0,
                    status=nm.NotificationStatus.WARNING,
                    button_infos=[ok_button, cancel_button]
                )

    """

    global _global_instance
    if _global_instance and _global_instance():
        ni = NotificationInfo(text, hide_after_timeout, duration, status, button_infos)
        return _global_instance().post_notification(ni)

    return None


def destroy_all_notifications():
    global _global_instance
    if _global_instance and _global_instance():
        return _global_instance().destroy_all_notifications()


def get_all_notifications():
    global _global_instance
    if _global_instance and _global_instance():
        return _global_instance().get_all_notifications()


class NotificationManagerExtension(omni.ext.IExt):
    def on_startup(self):
        global _global_instance
        _global_instance = weakref.ref(self)
        self._notification_manager = NotificationManager()
        self._notification_manager.on_startup()

    def on_shutdown(self):
        global _global_instance
        _global_instance = None
        self._notification_manager.on_shutdown()
        self._notification_manager = None
    
    def post_notification(self, notification_info: NotificationInfo):
        return self._notification_manager.post_notification(notification_info)

    def destroy_all_notifications(self):
        return self._notification_manager.destroy_all_notifications()

    def get_all_notifications(self):
        return self._notification_manager.get_all_notifications()
