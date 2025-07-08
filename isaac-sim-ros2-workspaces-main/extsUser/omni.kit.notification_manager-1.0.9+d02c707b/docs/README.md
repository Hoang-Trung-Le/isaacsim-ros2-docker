# omni.kit.notification_manager

## Introduction

This extension provides simple interface to post notifications.

## Example

        >>> import omni.kit.notification_manager as nm
        >>>
        >>> ok_button = nm.NotificationButtonInfo("OK", on_complete=None)
        >>> cancel_button = nm.NotificationButtonInfo("CANCEL", on_complete=None)
        >>> notification_info = nm.post_notification(
                    "Notification Example", hide_after_timeout=False, duration=0,
                    status=nm.NotificationStatus.WARNING, button_infos=[ok_button, cancel_button])