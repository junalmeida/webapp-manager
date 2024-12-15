#!/usr/bin/python3
import os
import sys
from setproctitle import setproctitle
from webapps_manager.WebAppManagerWindow import WebAppManagerWindow
from webapps_manager.common import APP, APP_ID
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QFile, QIODeviceBase
from PySide6 import QtAsyncio
from PySide6.QtUiTools import QUiLoader
from webapps_manager.WebAppManager import WebAppManager
from webapps_manager.common import _

def loadUi(file_name: str):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    ui_file_name =os.path.join(dir_name, file_name)
    ui_file = QFile(ui_file_name)  

    try:
        if not ui_file.open(QIODeviceBase.OpenModeFlag.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}", sys.stderr)
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)

        if not window:
            print(loader.errorString(), sys.stderr)
            sys.exit(-1)
        return window
    except Exception as e:
        print(f"Error loading {ui_file_name}: {e}", sys.stderr)
        sys.exit(-1)
    finally:
        ui_file.close()

def main():
    """Initializes and manages the application execution"""
    setproctitle(APP)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)
    app = QApplication(sys.argv)
    app.setApplicationName(_("Web Apps Manager"))
    app.setDesktopFileName(APP_ID)
    app.quitOnLastWindowClosed()
    
    manager = WebAppManager()
    qtwindow = loadUi("WebAppManagerWindow.ui")
    mainWindow = WebAppManagerWindow(app, qtwindow, manager)
    mainWindow.show()

    QtAsyncio.run(handle_sigint=True, quit_qapp=True)


if __name__ == "__main__":
    main()