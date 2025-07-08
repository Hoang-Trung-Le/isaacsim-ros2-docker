import asyncio
import carb
import omni.kit.app
import omni.ui as ui

from typing import List

from .notification_info import NotificationInfo, NotificationStatus
from .prompt import Prompt


SETTINGS_DISABLE_NOTIFICATIONS = "/exts/omni.kit.notification_manager/disable_notifications"
SETTINGS_LOOP_IDLE_TIME = "/exts/omni.kit.notification_manager/loopIdleTimeInSeconds"


class Notification:
    """Handler of notification"""

    def __init__(self, notification_info: NotificationInfo, notification_manager):
        """Internal constructor"""

        self._prompt = None
        self._notification_info = notification_info
        self._time_passed = 0
        self._notification_mananger = notification_manager
        self._is_warming = True

    def destroy(self):
        self._is_warming = False
        self._notification_info = None
        if self._prompt:
            self._prompt.destroy()
            self._prompt = None

        if self._notification_mananger:
            self._notification_mananger.remove_notification(self)
        self._notification_mananger = None

    def _step_and_check(self, dt):
        if not self._prompt:
            return True

        if self._notification_info.hide_after_timeout:
            if self._time_passed >= self._notification_info.duration:
                return True

            self._time_passed += dt

        return False

    async def _docking_to(self, window_x, window_y, window_width, window_height, offset_y=0):
        if self._prompt:
            await self._prompt.docking_to(window_x, window_y, window_width, window_height, offset_y)

    def _hide(self):
        if self._prompt:
            self._prompt.hide()

    async def _pre_warming(self):
        self._prompt = Prompt(self._notification_info)

        # Set it to a corner pos
        self._prompt.position_x = 100000
        self._prompt.position_y = 100000
        # FIXME: After creation, the notification window still
        # does not have the correct width/height. It needs to
        # show and wait for the first draw to get correct width/height.
        # The following code shows it and all notification will
        # be transparent at the start. After getting correct widht/height,
        # it will be positioned to correct position later.
        self._prompt.show()
        self._is_warming = False

        async def _warming():
            while not self._notification_mananger._shutdown and (self._prompt.width == 0.0 or self._prompt.height == 0.0):
                await omni.kit.app.get_app().next_update_async()
            self._hide()

            if not self._notification_mananger._shutdown:
                self._notification_mananger._pending_notifications.append(self)

        await _warming()

    @property
    def _dismissed(self):
        return self._prompt is None or not self._prompt.visible

    @property
    def _hovered(self):
        return self._prompt and self._prompt.hovered

    @property
    def info(self):
        return self._notification_info

    def dismiss(self):
        self.destroy()

    @property
    def dismissed(self):
        return not self._is_warming and self._prompt is None


class NotificationManager:
    def on_startup(self):
        self._max_showed_notifications = 5
        self._max_throttle_notifications = self._max_showed_notifications + 2
        self._pre_warming_notifications: List[Notification] = []
        self._pending_notifications: List[Notification] = []
        self._notifications: List[Notification] = []
        self._timer_task = None
        self._shutdown = False
        self._docking_window_width = 0
        self._docking_window_height = 0
        self._docking_window_pos_x = 0
        self._docking_window_pos_y = 0
        self._settings = carb.settings.get_settings()
        self._loop_idle_time_in_seconds = float(self._settings.get(SETTINGS_LOOP_IDLE_TIME))

        async def timer_fn():
            while not self._shutdown:

                """
                For each notification, it has 3 stages:
                1. When it's created, it will be put in the pre-warming queue.
                Pre-warming is a WA to calculate the real size of prompt before it's positioning.
                2. After pre-warming, it will be put to pending queue and waits to be displayed there.
                3. If there is vacancy (determined by _max_showed_notifications), it will be displayed to viewport finally.
                """
                showed_notifications = len(self._pending_notifications) + len(self._notifications)
                new_notifications = max(self._max_throttle_notifications - showed_notifications, 0)
                new_notifications = min(len(self._pre_warming_notifications), new_notifications)
                for _ in range(new_notifications):
                    notification = self._pre_warming_notifications.pop(0)
                    await notification._pre_warming()

                # To avoid flooding notification queue, all others will be flushed to console.
                for notification in self._pre_warming_notifications:
                    if notification.info.status == NotificationStatus.INFO:
                        carb.log_info(notification.info.text)
                    else:
                        carb.log_warn(notification.info.text)
                    notification.destroy()
                self._pre_warming_notifications.clear()

                changed = self._on_docking_window_changed()
                pending_to_remove = []
                for notification in self._notifications:
                    if (
                        (notification._step_and_check(0.5) and not notification._hovered) or
                        notification._dismissed
                    ):
                        pending_to_remove.append(notification)

                if len(pending_to_remove):
                    changed = True
                for item in pending_to_remove:
                    item.destroy()

                num_current_notifications = len(self._notifications)
                if num_current_notifications < self._max_showed_notifications:
                    new_added = self._max_showed_notifications - num_current_notifications
                else:
                    new_added = 0
                num_pending_notifications = len(self._pending_notifications)
                new_added = min(new_added, num_pending_notifications)
                for i in range(new_added):
                    notification = self._pending_notifications.pop(0)
                    self._notifications.append(notification)

                if new_added > 0:
                    changed = True

                if changed:
                    offset_y = 0
                    for notification in self._notifications:
                        await notification._docking_to(self._docking_window_pos_x, self._docking_window_pos_y, self._docking_window_width, self._docking_window_height, offset_y)
                        offset_y += notification._prompt.height + 5

                # Idle time
                if self._loop_idle_time_in_seconds > 0.0:
                    await asyncio.sleep(self._loop_idle_time_in_seconds)
                else:
                    # Wait one frame update at least.
                    await omni.kit.app.get_app().next_update_async()

        self._timer_task = asyncio.ensure_future(timer_fn())

    def on_shutdown(self):
        self._shutdown = True
        if self._timer_task:
            self._timer_task.cancel()
            self._timer_task = None
        for notification in self._notifications:
            notification.destroy()

        for notification in self._pending_notifications:
            notification.destroy()

        for notification in self._pre_warming_notifications:
            notification.destroy()

        self._notifications.clear()
        self._pending_notifications.clear()
        self._pre_warming_notifications.clear()

    def post_notification(self, notification_info: NotificationInfo):
        notification = Notification(notification_info, self)

        # OM-87367: options to disable all notifications.
        disable_all_notifications = self._settings.get(SETTINGS_DISABLE_NOTIFICATIONS)
        if disable_all_notifications:
            if notification.info.status == NotificationStatus.INFO:
                carb.log_info(notification.info.text)
            else:
                carb.log_warn(notification.info.text)
            notification.destroy()
        else:
            self._pre_warming_notifications.append(notification)

        # Still returns the handle of notification.
        return notification

    def remove_notification(self, notification: Notification):
        try:
            if notification in self._notifications:
                self._notifications.remove(notification)

            if notification in self._pending_notifications:
                self._pending_notifications.remove(notification)

            if notification in self._pre_warming_notifications:
                self._pre_warming_notifications.remove(notification)
        except ValueError:
            pass

    def destroy_all_notifications(self):
        for notification in self._notifications:
            notification.destroy()

        for notification in self._pending_notifications:
            notification.destroy()

        for notification in self._pre_warming_notifications:
            notification.destroy()

        self._notifications.clear()
        self._pending_notifications.clear()
        self._pre_warming_notifications.clear()

    def get_all_notifications(self):
        return self._notifications + self._pending_notifications + self._pre_warming_notifications

    def _on_docking_window_changed(self):
        viewport = ui.Workspace.get_window("Viewport")
        if viewport and viewport.visible:
            window_position_x = viewport.position_x
            window_position_y = viewport.position_y
            window_width = viewport.width
            window_height = viewport.height
        else:
            window_position_x = 0
            window_position_y = 0
            window_width = ui.Workspace.get_main_window_width()
            window_height = ui.Workspace.get_main_window_height()

        if ((self._docking_window_pos_x != window_position_x) or
            (self._docking_window_pos_y != window_position_y) or
            (self._docking_window_width != window_width) or
            (self._docking_window_height != window_height)):
            self._docking_window_pos_x = window_position_x
            self._docking_window_pos_y = window_position_y
            self._docking_window_width = window_width
            self._docking_window_height = window_height

            return True

        return False
