#!/usr/bin/python3
import os
import shutil
import sys
from setproctitle import setproctitle
from webapps_manager.WebAppManagerWindow import WebAppManagerWindow
from webapps_manager.common import APP, APP_ID, IS_FLATPAK, _
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QFile, QIODeviceBase
from PySide6 import QtAsyncio
from PySide6.QtUiTools import QUiLoader
from webapps_manager.WebAppManager import WebAppManager


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

def apply_menus():        
    if IS_FLATPAK:
        MENUS_PATH = os.path.join(os.getenv("HOME") or "", ".config", "menus", "applications-merged")
        MENUS_FILE = os.path.join(MENUS_PATH, f"{APP_ID}.menu")

        DIR_PATH = os.path.join(os.getenv("HOME") or "", ".local", "share", "desktop-directories")
        DIR_FILE = os.path.join(DIR_PATH, f"{APP_ID}.directory")
        update=False
        if not os.path.exists(MENUS_FILE):
            os.makedirs(MENUS_PATH, exist_ok=True)
            shutil.copyfile(f"/app/etc/xdg/menus/applications-merged/{APP_ID}.menu", MENUS_FILE)
            update=True
        if not os.path.exists(DIR_FILE):
            os.makedirs(DIR_PATH, exist_ok=True)
            shutil.copyfile(f"/app/share/desktop-directories/{APP_ID}.directory", DIR_FILE)    
            update=True
        if update:
            os.system("flatpak-spawn --host xdg-desktop-menu forceupdate")

def main():
    """Initializes and manages the application execution"""
    setproctitle(APP)
    apply_menus()

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