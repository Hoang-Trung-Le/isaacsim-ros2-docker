# Public API for module omni.kit.notification_manager:

## Classes

- class NotificationButtonInfo
  - def __init__(self, text, on_complete: Callable[[None], None] = None)
  - [property] def text(self)
  - [property] def handler(self)

- class NotificationStatus
  - WARNING: int
  - INFO: int

## Functions

- def post_notification(text, hide_after_timeout = True, duration = 3, status = NotificationStatus.INFO, button_infos = [])
- def destroy_all_notifications()
- def get_all_notifications()
