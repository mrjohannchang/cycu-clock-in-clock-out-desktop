import atexit
import logging
import sys

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication

import cycu_cico_sdk as sdk
from . import ui
from . import ui_model


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    atexit.register(sdk.SimpleCycuCico.clean_up)
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app: QApplication = QApplication(sys.argv)
    _ = ui.MainWindow().inflate().bind(ui_model.MainWindowModel()).show()
    return app.exec_()
