# Notification Settings

## /exts/omni.kit.notification_manager/loopIdleTimeInSeconds

When there are multiple notifications, need to adjust dock position to make sure they are at bottom-right of viewport or main window if new notification comes or old one closes.

Idle time (in seconds) to is the interval to check these changes. If no more than 0 seconds, will check every frame.


## /exts/omni.kit.notification_manager/disable_notifications

Default False to post notification in viewport or main window (if viewport invisible).

If True, output to log instead of post notification.