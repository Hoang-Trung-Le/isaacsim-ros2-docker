import asyncio
import carb.settings
import omni.kit.test
import omni.ui as ui
import omni.kit.notification_manager as nm

from omni.ui.tests.test_base import OmniUiTest
from pathlib import Path
from threading import Thread


CURRENT_PATH = Path(__file__).parent.joinpath("../../../../data")


class TestNotificationManagerUI(OmniUiTest):
    async def setUp(self):
        await super().setUp()
        self._golden_img_dir = CURRENT_PATH.absolute().resolve().joinpath("tests")
        self._all_notifications = []
        self._settings = carb.settings.get_settings()
        self._original_value = self._settings.get_as_int("/persistent/app/viewport/displayOptions")
        self._settings.set_int("/persistent/app/viewport/displayOptions", 0)
        self._settings.set("/exts/omni.kit.notification_manager/loopIdleTimeInSeconds", 0.0)

        # Create test area
        await self.create_test_area(1024, 1024)
        window_flags = ui.WINDOW_FLAGS_NO_SCROLLBAR | ui.WINDOW_FLAGS_NO_TITLE_BAR | ui.WINDOW_FLAGS_NO_RESIZE
        self._test_window = ui.Window(
            "Viewport",
            dockPreference=ui.DockPreference.DISABLED,
            flags=window_flags,
            width=1024,
            height=1024,
            position_x=0,
            position_y=0,
        )
        # Override default background
        self._test_window.frame.set_style({"Window": {"background_color": 0xFF000000, "border_color": 0x0, "border_radius": 0}})

        await omni.kit.app.get_app().next_update_async()
        await omni.kit.app.get_app().next_update_async()

    # After running each test
    async def tearDown(self):
        self._golden_img_dir = None
        for notification in self._all_notifications:
            notification.dismiss()
        self._all_notifications.clear()

        # Wait for 1s to make sure all notifications are disappeared.
        await asyncio.sleep(1)
        self._test_window = None
        self._settings.set_int("/persistent/app/viewport/displayOptions", self._original_value)
        await super().tearDown()

    async def _wait(self, frames=10):
        for i in range(frames):
            await omni.kit.app.get_app().next_update_async()

    async def test_create_multiple_notifications(self):
        self._all_notifications.append(nm.post_notification("test", duration=2))
        self._all_notifications.append(nm.post_notification("test1", duration=2, status=nm.NotificationStatus.WARNING))
        self._all_notifications.append(nm.post_notification("test2", duration=2))
        await self._wait()
        await asyncio.sleep(1.0)
        # Wait 10 frames for notifications to show up.
        await self.finalize_test(golden_img_dir=self._golden_img_dir, golden_img_name="test_create_multiple_notifications.png")

    async def test_auto_hide_notifications(self):
        self._all_notifications.append(nm.post_notification("test", duration=0.5))
        await self._wait()
        # Watis for 2s for notification to hide
        await asyncio.sleep(2)
        await self.finalize_test(golden_img_dir=self._golden_img_dir, golden_img_name="test_auto_hide_notifications.png")

    async def test_multiple_auto_hide_notifications(self):
        self._all_notifications.append(nm.post_notification("test", duration=0.5))
        self._all_notifications.append(nm.post_notification("test1", duration=0.5))
        self._all_notifications.append(nm.post_notification("test2", duration=0.5))
        await self._wait()
        # Watis for 2s for notification to hide
        await asyncio.sleep(2)
        await self.finalize_test(golden_img_dir=self._golden_img_dir, golden_img_name="test_multiple_auto_hide_notifications.png")

    async def test_create_non_auto_hide_notifications(self):
        self._all_notifications.append(nm.post_notification("test", duration=0.5, hide_after_timeout=False))
        await self._wait()
        # Watis for 2s for notification and check if it's still shown.
        await asyncio.sleep(2)
        await self.finalize_test(golden_img_dir=self._golden_img_dir, golden_img_name="test_non_auto_hide_notifications.png")

    async def test_manual_hide_notifications(self):
        for i in range(100):
            self._all_notifications.append(nm.post_notification("test", duration=1))

        # Wait and show
        await self._wait()
        await asyncio.sleep(2)

        # Dismiss them manually, after this, all notifications will be dismissed
        for n in self._all_notifications:
            n.dismiss()
        self._all_notifications.clear()

        # Creates another notification and shows it should work.
        self._all_notifications.append(nm.post_notification("test100", duration=10))
        await self._wait()
        await asyncio.sleep(2)

        await self.finalize_test(golden_img_dir=self._golden_img_dir, golden_img_name="test_manual_hide_notifications.png")

    async def test_multithreads_post(self):
        def run():
            nm.post_notification("test multiple threads")

        t = Thread(target=run)
        try:
            t.start()
            # 2s is enough to show notification
            await asyncio.sleep(2.0)
            await self.finalize_test(golden_img_dir=self._golden_img_dir, golden_img_name="test_multithreads_post.png")
        except Exception:
            pass
        finally:
            t.join()

    async def test_destroy_all_notifications(self):
        for i in range(5):
            nm.post_notification(f"test {i}", duration=9999, status=nm.NotificationStatus.INFO)

        # Wait and show
        await self._wait()
        await asyncio.sleep(2)

        self.assertEqual(len(nm.get_all_notifications()), 5)
        nm.destroy_all_notifications()
        await self._wait()
        self.assertEqual(nm.get_all_notifications(), [])

        await self._wait()
