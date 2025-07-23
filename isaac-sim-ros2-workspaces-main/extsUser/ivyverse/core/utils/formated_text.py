from typing import List

import carb
import omni.kit.clipboard as clipboard
import omni.ui as ui

try:
    import omni.kit.widget.text_editor as te
except ImportError:
    te = None


class ImagePreview(ui.Window):
    def __init__(self, image: str, *args, **kwargs):
        super().__init__("Preview", *args, **kwargs)
        self._image = image
        self.frame.set_build_fn(self._build_ui)

        self.move_to_new_os_window()

    def _build_ui(self):
        with ui.VStack():
            ui.Image(self._image)


class FormatedImages:
    def __init__(self, images: List[str], *args, **kwargs):
        self._frame = ui.Frame(*args, **kwargs)
        self._image_preview = None
        self._images = images
        num_images = len(images)
        size = 512
        if num_images == 1:
            size = 512
        elif num_images == 2:
            size = 256

        with self._frame:
            with ui.VGrid(height=0, column_width=size, row_height=size, spacing=10):
                for image in self._images:
                    ui.Image(
                        image,
                        width=size,
                        height=size,
                        mouse_pressed_fn=lambda x, y, b, k, image=image: self._show_image(image),
                    )

    def _show_image(self, image: str):
        self._image_preview = ImagePreview(image, width=1024, height=1024)


class FormatedCode:
    def __init__(self, text: str, *args, **kwargs):
        self._frame = ui.Frame(*args, **kwargs)
        self._editor = None
        self._label = None

        self.text = text

        with self._frame:
            self._label, self._editor = self._build_code_ui()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._type = "code"

        if text.startswith("python"):
            self._type = "python"
            text = text[6:]
        elif text.startswith("bash"):
            self._type = "bash"
            text = text[4:]
        if te is not None and text.startswith("\n"):
            text = text[1:]
        if te is not None and not text.endswith("\n"):
            text += "\n"

        self._text = text

        if self._editor:
            # It drives the height of the text editor
            self._label.text = "\n" * (text.count("\n") + 1)
            self._editor.text = text
        elif self._label:
            self._label.text = text

    def _copy_code(self, text: str):
        clipboard.copy(text)

    def _exec_code(self, text: str):
        if self._type == "bash":
            pass

        elif self._type == "python" or True:
            try:
                import omni.usd

                text = "import omni.usd\n" + text
            except ImportError:
                pass

            text = text.replace("Usd.Stage.CreateInMemory()", "omni.usd.get_context().get_stage()")

            try:
                # TODO: Put it to a separate extension
                from omni.ai.langchain.agent.usd_code.modifiers.double_run_usd_code_gen_interpreter_modifier import (
                    DoubleRunUSDCodeGenInterpreterModifier,
                )
            except ImportError:
                DoubleRunUSDCodeGenInterpreterModifier = None

            if DoubleRunUSDCodeGenInterpreterModifier is not None:
                code_interpreter = DoubleRunUSDCodeGenInterpreterModifier()
                code_snippet_run = code_interpreter._fix_before_run(text)
                execution_result = code_interpreter._run(code_snippet_run)
                print(execution_result)
            else:
                try:
                    exec(text, globals())
                except Exception as e:
                    return_string = f"This Code container Error, you need to fix it\nthe error is {e}"
                    carb.log_warn(return_string)

    def _build_code_ui(self):
        with ui.VStack(height=0):
            with ui.ZStack():
                ui.Rectangle(name="code-header-background")
                with ui.HStack():
                    with ui.VStack():
                        ui.Spacer()
                        ui.Label(f"   {self._type.capitalize()}", name="code_language", height=0, width=0)
                        ui.Spacer()
                    ui.Spacer()
                    # often the code does show as python even if it is
                    if self._type == "python" or True:
                        ui.Button(
                            tooltip="Execute code",
                            name="execute",
                            image_width=20,
                            image_height=25,
                            width=0,
                            clicked_fn=lambda text=self._text: self._exec_code(text),
                        )
                    ui.Button(
                        tooltip="Copy code",
                        name="copy-code",
                        image_width=25,
                        image_height=25,
                        width=0,
                        clicked_fn=lambda text=self._text: self._copy_code(text),
                    )
            with ui.ZStack():
                ui.Rectangle(name="code-background")
                with ui.HStack(height=0):
                    ui.Spacer(width=10)
                    with ui.VStack():
                        with ui.ZStack():
                            label = ui.Label(
                                self._text,
                                height=0,
                                style_type_name_override="Label.Code",
                                word_wrap=True,
                                alignment=ui.Alignment.LEFT_TOP,
                            )
                            if te is not None:
                                # Keep the old label so it drives the height
                                # One more line for the scroll bar
                                label.text = "\n" * (label.text.count("\n") + 2)

                                editor = te.TextEditor(
                                    text=self._text,
                                    read_only=True,
                                    style_type_name_override="Label.Code",
                                    alignment=ui.Alignment.LEFT_TOP,
                                    syntax=te.TextEditor.Syntax.PYTHON,
                                )
                            else:
                                editor = None
                        ui.Spacer(height=10)
                    ui.Spacer(width=10)
        return label, editor


class FormatedText:
    def __init__(self, text, *args, **kwargs):
        self._text = text
        self._frame = ui.Frame(*args, **kwargs)
        self._frame.set_build_fn(self._build_ui)
        self._label: ui.Label = None
        self._code: ui.Label = None
        self._style_name = kwargs.get("style_name", "Label.User")
        self._scroll_to_bottom = kwargs.get("scroll_to_bottom", True)
        self._scroll_target = None

        self._part_count = 0
        self._latest_part = None

        with self._frame:
            self._build_ui()

    def update(self, text):
        self._text = text
        parts = self._text_parts(text)
        part_count = len(parts)
        if self._latest_part and self._part_count == part_count:
            self._latest_part.text = parts[-1]
            # Always scroll to the bottom
            if self._scroll_target:
                self._scroll_target.scroll_here_y(1.0)
            else:
                self._frame.scroll_here_y(1.0)
        else:
            self._part_count = part_count
            self._frame.rebuild()

    @property
    def visible(self):
        if self._frame:
            return self._frame.visible

    @visible.setter
    def visible(self, value: bool):
        if self._frame:
            self._frame.visible = value

    def _text_parts(self, text: str, delimiter: str = "```", tag: str = "<|python_tag|>") -> List[str]:
        if tag and text.startswith(tag):
            return text.split(tag)
        return text.split(delimiter)

    def _url_parts(self, text: str) -> List[str]:
        import re

        urls = re.findall(r"(https?://\S+)", text)
        return urls

    def _build_text_ui(self, text: str):
        return ui.Label(
            text, height=0, style_type_name_override=self._style_name, word_wrap=True, alignment=ui.Alignment.LEFT_TOP
        )

    def _build_ui(self):
        text = self._text
        if not self._text:
            return

        parts = self._text_parts(text)
        with ui.VStack():
            ui.Spacer(height=5)
            for i, part in enumerate(parts):
                # check if the index is even or odd
                if i % 2 == 0:
                    self._latest_part = self._build_text_ui(part)
                else:
                    self._latest_part = FormatedCode(part)

            show_images = True
            if show_images:
                import re

                image_c_urls = re.findall(r"C:[^\s]+?\.(?:jpg|png|gif)", text)
                image_http_urls = re.findall(r"http[^\s]+?\.(?:jpg|png|gif)", text)
                FormatedImages(image_c_urls)
                FormatedImages(image_http_urls)

            # Always scroll to the bottom
            if self._scroll_to_bottom:
                self._scroll_target = ui.Spacer(height=ui.Pixel(1))
                self._scroll_target.scroll_here_y(1.0)
