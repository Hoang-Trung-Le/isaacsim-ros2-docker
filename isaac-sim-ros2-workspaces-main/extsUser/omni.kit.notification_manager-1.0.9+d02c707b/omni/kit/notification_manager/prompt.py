import weakref
import omni.ui as ui
import omni.kit.app
import uuid
from .notification_info import NotificationStatus, NotificationInfo
from .icons import Icons


HOVER_AREA_TRANSPARENT_STYLE = {
    "background_color": 0x0,
    "background_gradient_color": 0x0,
    "background_selected_color": 0x0,
    "border_color": 0x0,
    "color": 0x0,
    "selected_color": 0x0,
    "secondary_color": 0x0,
    "secondary_selected_color": 0x0,
    "debug_color": 0x0
}

HOVER_AREA_DEFAULT_STYLE = {
    "Rectangle::hover_area_info": {"background_color": 0xFFE2B170, "border_radius": 10},
    "Rectangle::hover_area_warning": {"background_color": 0xFF5EC7E8, "border_radius": 10},
    "Label::text": {"font_size": 14, "color": 0xFF000000},
    "Image::status_warning": {"image_url": Icons().get("warning"), "color": 0xFF000000},
    "Image::status_info": {"image_url": Icons().get("info"), "color": 0xFF000000},
    "Button:hovered": {"background_color": 0xFF9E9E9E},
}


class Prompt:
    def __init__(self, notification_info: NotificationInfo):
        self._notification_info = notification_info
        self._build_ui(
            notification_info.text, notification_info.status,
            notification_info.button_infos
        )

        self._docking_window_x = 0
        self._docking_window_y = 0
        self._docking_window_width = 0
        self._docking_window_height = 0
        self._hovered = False

    def destroy(self):
        self._notification_info = None
        self._window.destroy()
        self._window = None

    def __enter__(self):
        self._window.show()
        return self

    def __exit__(self, type, value, trace):
        self._window.hide()

    def show(self):
        self._window.visible = True

    def hide(self):
        self._window.visible = False

    @property
    def hovered(self):
        return self._hovered

    @property
    def visible(self):
        return self._window.visible

    @visible.setter
    def visible(self, value):
        self._window.visible = value

    @property
    def position_x(self):
        return self._window.position_x

    @position_x.setter
    def position_x(self, value):
        self._window.position_x = value

    @property
    def position_y(self):
        return self._window.position

    @position_y.setter
    def position_y(self, value):
        self._window.position_y = value

    @property
    def width(self):
        return self._window.width

    @property
    def height(self):
        return self._window.height

    @property
    def window_id(self):
        """Id that can be used for ui_test to query notification window."""

        return self._window_id

    async def docking_to(self, window_x, window_y, window_width, window_height, offset_y=0):
        self._docking_window_x = window_x
        self._docking_window_y = window_y
        self._docking_window_width = window_width
        self._docking_window_height = window_height
        self._window.visible = True
        # FIXME: No idea why this works. It needs to wait for the width/height to be stabalized.
        await omni.kit.app.get_app().next_update_async()
        position_x = self._docking_window_x + self._docking_window_width - self._window.width - 16
        position_y = self._docking_window_y + self._docking_window_height - self._window.height - 16 - offset_y
        self._window.position_x = position_x if position_x > 0 else 0
        self._window.position_y = position_y if position_y > 0 else 0
        if self._notification_info.status == NotificationStatus.INFO:
            self._window.frame.set_style({"Window": {"background_color": 0xFF75542A, "border_radius": 10}})
        else:
            self._window.frame.set_style({"Window": {"background_color": 0xFF2D5CA1, "border_radius": 10}})
        self._layout.set_style(HOVER_AREA_DEFAULT_STYLE)

    def _build_ui(self, text, status, button_details):
        self._window_id = str(uuid.uuid1())
        self._window = ui.Window(self._window_id, visible=False, height=0, dockPreference=ui.DockPreference.DISABLED)
        self._window.flags = (
            ui.WINDOW_FLAGS_NO_COLLAPSE
            | ui.WINDOW_FLAGS_NO_RESIZE
            | ui.WINDOW_FLAGS_NO_SCROLLBAR
            | ui.WINDOW_FLAGS_NO_RESIZE
            | ui.WINDOW_FLAGS_NO_MOVE
            | ui.WINDOW_FLAGS_NO_TITLE_BAR
            | ui.WINDOW_FLAGS_NO_CLOSE
            | ui.WINDOW_FLAGS_NO_FOCUS_ON_APPEARING
        )

        def _button_handler(handler):
            self.hide()
            if handler:
                handler()

        weak_self = weakref.ref(self)

        def _on_hovered(hovered):
            if not weak_self():
                return
            weak_self()._hovered = hovered

        self._window.frame.style = HOVER_AREA_TRANSPARENT_STYLE
        with self._window.frame:
            self._layout = ui.ZStack(style=HOVER_AREA_DEFAULT_STYLE, height=0)
            with self._layout:
                if status == NotificationStatus.INFO:
                    hover_area = ui.Rectangle(name="hover_area_info")
                else:
                    hover_area = ui.Rectangle(name="hover_area_warning")
                hover_area.set_mouse_hovered_fn(_on_hovered)
                with ui.VStack(height=0):
                    ui.Spacer(height=5)
                    with ui.HStack(height=0):
                        if status == NotificationStatus.INFO:
                            name = "status_info"
                        else:
                            name = "status_warning"
                        ui.Spacer(width=5)
                        ui.Image(width=20, alignment=ui.Alignment.CENTER, name=name)
                        ui.Spacer(width=10)
                        ui.Label(
                            text, name="text", word_wrap=True, width=self._window.width - 44,
                            height=0, alignment=ui.Alignment.LEFT
                        )
                        ui.Spacer()

                    if button_details:
                        button_width = 60 if len(button_details) >=3 else 120
                        ui.Spacer(width=0, height=10)
                        with ui.HStack(height=0):
                            ui.Spacer()
                            button = ui.Button(button_details[0].text, width=button_width, height=0)
                            button.set_clicked_fn(lambda a=button_details[0].handler: _button_handler(a))
                            for i in range(len(button_details) - 1):
                                ui.Spacer(width=5)
                                button_info = button_details[i + 1]
                                button = ui.Button(button_info.text, width=button_width, height=0)
                                button.set_clicked_fn(lambda a=button_info.handler: _button_handler(a))
                            ui.Spacer()
                    ui.Spacer(height=5)
