from __future__ import annotations

import importlib.resources
import pathlib
from typing import Optional

import cycu_cico_sdk as sdk
import PySide6.QtGui  # This is only for PyInstaller to parse properly
import PySide6.QtXml  # This is only for PyInstaller to parse properly
from PySide6.QtCore import QIODevice, QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QMainWindow

from .ui import UI
from .. import ui_model


class MainWindow(UI, sdk.Singleton):
    def __init__(self):
        super().__init__(parent=None)
        self.main_window: Optional[QMainWindow] = None
        self.main_window_model: Optional[ui_model.MainWindowModel] = None

        self.cover_image_label: Optional[QLabel] = None

    def bind(self, main_window_model: ui_model.MainWindowModel) -> MainWindow:
        super().bind(main_window_model)
        self.main_window_model = main_window_model
        return self

    def inflate(self, ui_path: Optional[str] = None) -> MainWindow:
        super().inflate(ui_path)

        main_window_ui: pathlib.Path
        with importlib.resources.path(__package__, 'main_window.ui') as main_window_ui:
            main_window_ui_qfile: QFile = QFile(str(main_window_ui))
            if not main_window_ui_qfile.open(QIODevice.ReadOnly):
                raise RuntimeError(f"Cannot open {main_window_ui}: {main_window_ui_qfile.errorString()}")
            qui_loader: QUiLoader = QUiLoader()
            self.main_window = qui_loader.load(main_window_ui_qfile)
            main_window_ui_qfile.close()
            if not self.main_window:
                raise RuntimeError(qui_loader.errorString())

        self.cover_image_label = getattr(self.main_window, 'cover_image_label')

        cover_image_path: pathlib.Path
        with importlib.resources.path(
                __package__, 'anime-anime-girls-hatsune-miku-vocaloid-wallpaper-preview.jpg') as cover_image_path:
            self.cover_image_label.setPixmap(str(cover_image_path))

        return self

    def show(self) -> MainWindow:
        super().show()
        self.main_window.show()
        return self
