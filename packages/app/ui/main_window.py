from __future__ import annotations

import datetime
import importlib.resources
import pathlib
from typing import Optional

from PySide6.QtCore import QIODevice, QFile, QTime
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QTimeEdit)
import PySide6.QtXml  # This is only for PyInstaller to parse the code properly

import cycu_cico_sdk as sdk
from .ui import UI
from .. import ui_model


class MainWindow(UI, sdk.Singleton):
    def __init__(self):
        super().__init__(parent=None)
        self.main_window: Optional[QMainWindow] = None
        self.main_window_model: Optional[ui_model.MainWindowModel] = None

        self.cover_image_label: Optional[QLabel] = None
        self.tab_widget: Optional[QTabWidget] = None

        self.account_line_edit: Optional[QLineEdit] = None
        self.password_line_edit: Optional[QLineEdit] = None
        self.clock_in_start_time_edit: Optional[QTimeEdit] = None
        self.clock_in_end_time_edit: Optional[QTimeEdit] = None
        self.clock_out_start_time_edit: Optional[QTimeEdit] = None
        self.clock_out_end_time_edit: Optional[QTimeEdit] = None
        self.exclude_weekends_check_box: Optional[QCheckBox] = None
        self.exclude_specific_dates_check_box: Optional[QCheckBox] = None
        self.specific_dates_text_edit: Optional[QPlainTextEdit] = None
        self.save_push_button: Optional[QPushButton] = None
        self.cancel_push_button: Optional[QPushButton] = None
        self.edit_push_button: Optional[QPushButton] = None

        self.status_label: Optional[QLabel] = None
        self.clock_in_push_button: Optional[QPushButton] = None
        self.clock_out_push_button: Optional[QPushButton] = None

        self.next_label: Optional[QLabel] = None
        self.stop_push_button: Optional[QPushButton] = None
        self.start_push_button: Optional[QPushButton] = None

    def bind(self, main_window_model: ui_model.MainWindowModel) -> MainWindow:
        super().bind(main_window_model)

        self.main_window_model = main_window_model

        self.tab_widget.setCurrentIndex(sdk.get_config().active_tab)
        self.account_line_edit.setText(main_window_model.account)
        self.password_line_edit.setText(main_window_model.password)
        self.clock_in_start_time_edit.setTime(QTime(
            main_window_model.clock_in_start_time.hour,
            main_window_model.clock_in_start_time.minute,
            main_window_model.clock_in_start_time.second))
        self.clock_in_end_time_edit.setTime(QTime(
            main_window_model.clock_in_end_time.hour,
            main_window_model.clock_in_end_time.minute,
            main_window_model.clock_in_end_time.second))
        self.clock_out_start_time_edit.setTime(QTime(
            main_window_model.clock_out_start_time.hour,
            main_window_model.clock_out_start_time.minute,
            main_window_model.clock_out_start_time.second))
        self.clock_out_end_time_edit.setTime(QTime(
            main_window_model.clock_out_end_time.hour,
            main_window_model.clock_out_end_time.minute,
            main_window_model.clock_out_end_time.second))
        self.exclude_weekends_check_box.setChecked(main_window_model.exclude_weekends)
        self.exclude_specific_dates_check_box.setChecked(main_window_model.exclude_specific_dates)
        self.specific_dates_text_edit.setPlainText('\n'.join(main_window_model.specific_dates))

        main_window_model.add_on_changed_observer(
            self.on_tab_bar_enabled_changed, 'tab_bar_enabled')
        main_window_model.add_on_changed_observer(
            self.on_account_line_edit_enabled_changed, 'account_line_edit_enabled')
        main_window_model.add_on_changed_observer(
            self.on_password_line_edit_enabled_changed, 'password_line_edit_enabled')
        main_window_model.add_on_changed_observer(
            self.on_clock_in_start_time_edit_enabled_changed, 'clock_in_start_time_edit_enabled')
        main_window_model.add_on_changed_observer(
            self.on_clock_in_end_time_edit_enabled_changed, 'clock_in_end_time_edit_enabled')
        main_window_model.add_on_changed_observer(
            self.on_clock_out_start_time_edit_enabled_changed, 'clock_out_start_time_edit_enabled')
        main_window_model.add_on_changed_observer(
            self.on_clock_out_end_time_edit_enabled_changed, 'clock_out_end_time_edit_enabled')
        main_window_model.add_on_changed_observer(
            self.on_exclude_weekends_check_box_enabled_changed, 'exclude_weekends_check_box_enabled')
        main_window_model.add_on_changed_observer(
            self.on_exclude_specific_dates_check_box_enabled_changed, 'exclude_specific_dates_check_box_enabled')
        main_window_model.add_on_changed_observer(
            self.on_specific_dates_text_edit_enabled_changed, 'specific_dates_text_edit_enabled')
        main_window_model.add_on_changed_observer(
            self.on_save_push_button_enabled_changed, 'save_push_button_enabled')
        main_window_model.add_on_changed_observer(
            self.on_cancel_push_button_enabled_changed, 'cancel_push_button_enabled')
        main_window_model.add_on_changed_observer(
            self.on_edit_push_button_enabled_changed, 'edit_push_button_enabled')

        main_window_model.add_on_changed_observer(
            self.on_clock_in_push_button_enabled_changed, 'clock_in_push_button_enabled')
        main_window_model.add_on_changed_observer(
            self.on_clock_out_push_button_enabled_changed, 'clock_out_push_button_enabled')

        main_window_model.add_on_changed_observer(
            self.on_stop_push_button_enabled_changed, 'stop_push_button_enabled')
        main_window_model.add_on_changed_observer(
            self.on_start_push_button_enabled_changed, 'start_push_button_enabled')

        main_window_model.add_on_changed_observer(
            self.on_account_model_changed, 'account')
        main_window_model.add_on_changed_observer(
            self.on_password_model_changed, 'password')
        main_window_model.add_on_changed_observer(
            self.on_clock_in_start_time_model_changed, 'clock_in_start_time')
        main_window_model.add_on_changed_observer(
            self.on_clock_in_end_time_model_changed, 'clock_in_end_time')
        main_window_model.add_on_changed_observer(
            self.on_clock_out_start_time_model_changed, 'clock_out_start_time')
        main_window_model.add_on_changed_observer(
            self.on_clock_out_end_time_model_changed, 'clock_out_end_time')
        main_window_model.add_on_changed_observer(
            self.on_exclude_weekends_model_changed, 'exclude_weekends')
        main_window_model.add_on_changed_observer(
            self.on_exclude_specific_dates_model_changed, 'exclude_specific_dates')
        main_window_model.add_on_changed_observer(
            self.on_specific_dates_model_changed, 'specific_dates')

        self.tab_widget.currentChanged.connect(self.on_active_tab_changed)
        self.account_line_edit.textChanged.connect(self.on_account_line_edit_changed)
        self.password_line_edit.textChanged.connect(self.on_password_line_edit_changed)
        self.clock_in_start_time_edit.timeChanged.connect(self.on_clock_in_start_time_edit_changed)
        self.clock_in_end_time_edit.timeChanged.connect(self.on_clock_in_end_time_edit_changed)
        self.clock_out_start_time_edit.timeChanged.connect(self.on_clock_out_start_time_edit_changed)
        self.clock_out_end_time_edit.timeChanged.connect(self.on_clock_out_end_time_edit_changed)
        self.exclude_weekends_check_box.stateChanged.connect(self.on_exclude_weekends_check_box_changed)
        self.exclude_specific_dates_check_box.stateChanged.connect(self.on_exclude_specific_dates_check_box_changed)
        self.specific_dates_text_edit.textChanged.connect(self.on_specific_dates_text_edit_changed)
        self.save_push_button.clicked.connect(self.on_save_push_button_clicked)
        self.cancel_push_button.clicked.connect(self.on_cancel_push_button_clicked)
        self.edit_push_button.clicked.connect(self.on_edit_push_button_clicked)

        self.tab_widget.setEnabled(main_window_model.tab_bar_enabled)
        self.account_line_edit.setEnabled(main_window_model.account_line_edit_enabled)
        self.password_line_edit.setEnabled(main_window_model.password_line_edit_enabled)
        self.clock_in_start_time_edit.setEnabled(main_window_model.clock_in_start_time_edit_enabled)
        self.clock_in_end_time_edit.setEnabled(main_window_model.clock_in_end_time_edit_enabled)
        self.clock_out_start_time_edit.setEnabled(main_window_model.clock_out_start_time_edit_enabled)
        self.clock_out_end_time_edit.setEnabled(main_window_model.clock_out_end_time_edit_enabled)
        self.exclude_weekends_check_box.setEnabled(main_window_model.exclude_weekends_check_box_enabled)
        self.exclude_specific_dates_check_box.setEnabled(main_window_model.exclude_specific_dates_check_box_enabled)
        self.specific_dates_text_edit.setEnabled(main_window_model.specific_dates_text_edit_enabled)
        self.save_push_button.setEnabled(main_window_model.save_push_button_enabled)
        self.cancel_push_button.setEnabled(main_window_model.cancel_push_button_enabled)
        self.edit_push_button.setEnabled(main_window_model.edit_push_button_enabled)

        self.clock_in_push_button.setEnabled(main_window_model.clock_in_push_button_enabled)
        self.clock_out_push_button.setEnabled(main_window_model.clock_out_push_button_enabled)

        self.stop_push_button.setEnabled(main_window_model.stop_push_button_enabled)
        self.start_push_button.setEnabled(main_window_model.start_push_button_enabled)
        return self

    def inflate(self, ui_path: Optional[pathlib.Path] = None) -> MainWindow:
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

        app_icon: pathlib.Path
        with importlib.resources.path(__package__, 'app.ico') as app_icon:
            self.main_window.setWindowIcon(QIcon(str(app_icon)))

        self.cover_image_label = getattr(self.main_window, 'cover_image_label')
        self.tab_widget = getattr(self.main_window, 'tab_widget')

        self.account_line_edit = getattr(self.main_window, 'account_line_edit')
        self.password_line_edit = getattr(self.main_window, 'password_line_edit')
        self.clock_in_start_time_edit = getattr(self.main_window, 'clock_in_start_time_edit')
        self.clock_in_end_time_edit = getattr(self.main_window, 'clock_in_end_time_edit')
        self.clock_out_start_time_edit = getattr(self.main_window, 'clock_out_start_time_edit')
        self.clock_out_end_time_edit = getattr(self.main_window, 'clock_out_end_time_edit')
        self.exclude_weekends_check_box = getattr(self.main_window, 'exclude_weekends_check_box')
        self.exclude_specific_dates_check_box = getattr(self.main_window, 'exclude_specific_dates_check_box')
        self.specific_dates_text_edit = getattr(self.main_window, 'specific_dates_text_edit')
        self.save_push_button = getattr(self.main_window, 'save_push_button')
        self.cancel_push_button = getattr(self.main_window, 'cancel_push_button')
        self.edit_push_button = getattr(self.main_window, 'edit_push_button')

        self.status_label = getattr(self.main_window, 'status_label')
        self.clock_in_push_button = getattr(self.main_window, 'clock_in_push_button')
        self.clock_out_push_button = getattr(self.main_window, 'clock_out_push_button')

        self.next_label = getattr(self.main_window, 'next_label')
        self.stop_push_button = getattr(self.main_window, 'stop_push_button')
        self.start_push_button = getattr(self.main_window, 'start_push_button')

        cover_image_path: pathlib.Path
        with importlib.resources.path(
                __package__, 'anime-anime-girls-hatsune-miku-vocaloid-wallpaper-preview.jpg') as cover_image_path:
            self.cover_image_label.setPixmap(str(cover_image_path))
        return self

    def show(self) -> MainWindow:
        super().show()
        self.main_window.show()
        return self

    def on_active_tab_changed(self, index: int):
        sdk.get_config().active_tab = index
        sdk.save_config()

    def on_tab_bar_enabled_changed(self, enabled: bool):
        self.tab_widget.tabBar().setEnabled(enabled)

    def on_account_line_edit_enabled_changed(self, enabled: bool):
        self.account_line_edit.setEnabled(enabled)

    def on_password_line_edit_enabled_changed(self, enabled: bool):
        self.password_line_edit.setEnabled(enabled)

    def on_clock_in_start_time_edit_enabled_changed(self, enabled: bool):
        self.clock_in_start_time_edit.setEnabled(enabled)

    def on_clock_in_end_time_edit_enabled_changed(self, enabled: bool):
        self.clock_in_end_time_edit.setEnabled(enabled)

    def on_clock_out_start_time_edit_enabled_changed(self, enabled: bool):
        self.clock_out_start_time_edit.setEnabled(enabled)

    def on_clock_out_end_time_edit_enabled_changed(self, enabled: bool):
        self.clock_out_end_time_edit.setEnabled(enabled)

    def on_exclude_weekends_check_box_enabled_changed(self, enabled: bool):
        self.exclude_weekends_check_box.setEnabled(enabled)

    def on_exclude_specific_dates_check_box_enabled_changed(self, enabled: bool):
        self.exclude_specific_dates_check_box.setEnabled(enabled)

    def on_specific_dates_text_edit_enabled_changed(self, enabled: bool):
        self.specific_dates_text_edit.setEnabled(enabled)

    def on_save_push_button_enabled_changed(self, enabled: bool):
        self.save_push_button.setEnabled(enabled)

    def on_save_push_button_clicked(self, checked: bool):
        self.main_window_model.save()

    def on_cancel_push_button_enabled_changed(self, enabled: bool):
        self.cancel_push_button.setEnabled(enabled)

    def on_cancel_push_button_clicked(self, checked: bool):
        self.main_window_model.cancel()

    def on_edit_push_button_enabled_changed(self, enabled: bool):
        self.edit_push_button.setEnabled(enabled)

    def on_edit_push_button_clicked(self, checked: bool):
        self.main_window_model.edit()

    def on_clock_in_push_button_enabled_changed(self, enabled: bool):
        self.clock_in_push_button.setEnabled(enabled)

    def on_clock_in_push_button_clicked(self, checked: bool):
        self.main_window_model.clock_in()

    def on_clock_out_push_button_enabled_changed(self, enabled: bool):
        self.clock_out_push_button.setEnabled(enabled)

    def on_clock_out_push_button_clicked(self, checked: bool):
        self.main_window_model.clock_out()

    def on_stop_push_button_enabled_changed(self, enabled: bool):
        self.stop_push_button.setEnabled(enabled)

    def on_stop_push_button_clicked(self, checked: bool):
        self.main_window_model.stop()

    def on_start_push_button_enabled_changed(self, enabled: bool):
        self.start_push_button.setEnabled(enabled)

    def on_start_push_button_clicked(self, checked: bool):
        self.main_window_model.start()

    def on_account_model_changed(self, value: str):
        self.account_line_edit.setText(value)

    def on_password_model_changed(self, value: str):
        self.password_line_edit.setText(value)

    def on_clock_in_start_time_model_changed(self, value: datetime.time):
        self.clock_in_start_time_edit.setTime(QTime(value.hour, value.minute, value.second))

    def on_clock_in_end_time_model_changed(self, value: datetime.time):
        self.clock_in_end_time_edit.setTime(QTime(value.hour, value.minute, value.second))

    def on_clock_out_start_time_model_changed(self, value: datetime.time):
        self.clock_out_start_time_edit.setTime(QTime(value.hour, value.minute, value.second))

    def on_clock_out_end_time_model_changed(self, value: datetime.time):
        self.clock_out_end_time_edit.setTime(QTime(value.hour, value.minute, value.second))

    def on_exclude_weekends_model_changed(self, value: bool):
        self.exclude_weekends_check_box.setChecked(2 if value else 0)

    def on_exclude_specific_dates_model_changed(self, value: int):
        self.exclude_specific_dates_check_box.setChecked(2 if value else 0)

    def on_specific_dates_model_changed(self, value: list[str]):
        self.specific_dates_text_edit.setPlainText('\n'.join(value))

    def on_account_line_edit_changed(self, value: str):
        self.main_window_model.account = value

    def on_password_line_edit_changed(self, value: str):
        self.main_window_model.password = value

    def on_clock_in_start_time_edit_changed(self, value: QTime):
        self.main_window_model.clock_in_start_time = datetime.time(value.hour(), value.minute(), value.second())

    def on_clock_in_end_time_edit_changed(self, value: QTime):
        self.main_window_model.clock_in_end_time = datetime.time(value.hour(), value.minute(), value.second())

    def on_clock_out_start_time_edit_changed(self, value: QTime):
        self.main_window_model.clock_out_start_time = datetime.time(value.hour(), value.minute(), value.second())

    def on_clock_out_end_time_edit_changed(self, value: QTime):
        self.main_window_model.clock_out_end_time = datetime.time(value.hour(), value.minute(), value.second())

    def on_exclude_weekends_check_box_changed(self, value: int):
        self.main_window_model.exclude_weekends = True if value else False

    def on_exclude_specific_dates_check_box_changed(self, value: int):
        self.main_window_model.exclude_specific_dates = True if value else False

    def on_specific_dates_text_edit_changed(self):
        self.main_window_model._specific_dates = self.specific_dates_text_edit.toPlainText().split('\n')
