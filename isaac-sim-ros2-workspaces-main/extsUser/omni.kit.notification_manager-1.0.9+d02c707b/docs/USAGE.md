# Usage Examples


## Notification Duration

By default, a notification will auto hide after 3 seconds.

The duration could be customized as:
```
import omni.kit.notification_manager as nm
# Auto hide notification 5 seconds later
nm.post_notification("This is a simple notification.", duration=5)
```

If required, notification could be there as:

```
import omni.kit.notification_manager as nm
# Do not auto hide notification.
# Instead, show a Dismiss button for user to close is manually.
nm.post_notification("This is a simple notification.", hide_after_timeout=False)
```

![](simple_notification_never_hide.png)

## Notification Status

By default, notification is shown as information.

Warning notification with different icon and background color is also supported:

```
import omni.kit.notification_manager as nm
# Show as warning
nm.post_notification("This is a warning notification.", status=nm.NotificationStatus.WARNING)
```

![](simple_warning_notification.png)

## Notification Buttons

By default, notification will show
- No button if auto hide
- A default button 'Dismiss" for user to close it if never hide

User could customize number of buttons, button text and extra action when notification closed.

```
import omni.kit.notification_manager as nm

def on_ok():
  print("OK button clicked!")

# Two buttons
# OK button to print a message when notification closed
# CANCEL button do nothing but close notification
ok_button = nm.NotificationButtonInfo("OK", on_complete=on_ok)
cancel_button = nm.NotificationButtonInfo("CANCEL", on_complete=None)
nm.post_notification("This is a simple notification.", button_infos=[ok_button, cancel_button])
```

![](notification_buttons.png)
