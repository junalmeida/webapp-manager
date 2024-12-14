
import os
from typing import cast
from PySide6.QtWidgets import QWidget, QToolBar, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QPixmap, QGuiApplication
from webapps_manager.icons import *
from webapps_manager.common import REFERENCE_DPI, SUPPORTED_BROWSERS, WebAppLauncher, APP
from webapps_manager.WebAppEdit import WebAppEdit
from webapps_manager.WebAppManager import WebAppManager

class WebAppManagerWindow:
    __window: QWidget

    def __init__(self, application: QGuiApplication, window: QWidget, manager: WebAppManager):
        self.__manager = WebAppManager()
        self.__window = window
    

        self.__window.setWindowTitle(application.applicationName()) 

        self.__toolbar = cast(QToolBar, self.__window.findChild(QToolBar, "toolBar"))

        self.__actionAdd = cast(QAction, self.__window.findChild(QAction, "actionAdd"))
        self.__actionAdd.triggered.connect(self.actionAdd_clicked)

        self.__actionRemove = cast(QAction, self.__window.findChild(QAction, "actionRemove"))
        self.__actionRemove.triggered.connect(self.actionRemove_clicked)
        self.__actionRemove.setEnabled(False)

        self.__actionEdit = cast(QAction, self.__window.findChild(QAction, "actionEdit"))
        self.__actionEdit.setEnabled(False)
        self.__actionEdit.triggered.connect(self.actionEdit_clicked)

        self.__actionLaunch = cast(QAction, self.__window.findChild(QAction, "actionLaunch"))
        self.__actionLaunch.setEnabled(False)
        self.__actionLaunch.triggered.connect(self.actionLaunch_clicked)

        self.__actionAbout = cast(QAction, self.__window.findChild(QAction, "actionAbout"))
        self.__actionAbout.triggered.connect(self.actionAbout_clicked)

        self.__stackedWidget = cast(QStackedWidget, self.__window.findChild(QStackedWidget, "stackedWidget"))
        self.__stackedWidget.currentChanged.connect(self.on_stackedWidget_currentChanged)

        self.__webAppEdit = WebAppEdit(self.__window, cast(QWidget, self.__window.findChild(QWidget, "editPage")), self.__manager, self.goFirstPage)

        self.__listWidget = cast(QListWidget, self.__window.findChild(QListWidget, "listWidget"))
        self.__listWidget.itemSelectionChanged.connect(self.on_itemSelectionChanged)
        self.__listWidget.itemDoubleClicked.connect(self.actionEdit_clicked)

        self.__ICON_X_SCALE_FACTOR = self.__window.logicalDpiX() / REFERENCE_DPI
        self.__ICON_Y_SCALE_FACTOR = self.__window.logicalDpiY() / REFERENCE_DPI
        self.goFirstPage()


    def show(self):
        self.__window.show()

    def goFirstPage(self):
        index = self.__listWidget.currentIndex()
        self.load_webapps()
        self.__listWidget.setCurrentIndex(index)
        self.__stackedWidget.setCurrentIndex(0)

    def actionAdd_clicked(self):
        self.__webAppEdit.createNew()
        self.__stackedWidget.setCurrentIndex(1)

    def actionRemove_clicked(self):
        listItem = self.__listWidget.currentItem()
        webapp = cast(WebAppLauncher, listItem.data(Qt.ItemDataRole.UserRole))        
        self.__webAppEdit.remove(webapp)

    def actionEdit_clicked(self):
        listItem = self.__listWidget.currentItem()
        webapp = cast(WebAppLauncher, listItem.data(Qt.ItemDataRole.UserRole))
        self.__webAppEdit.edit(webapp)
        self.__stackedWidget.setCurrentIndex(1)

    def actionLaunch_clicked(self):
        print("Launch clicked")


    def actionAbout_clicked(self):
        QMessageBox.about(self.__window, "About Web Apps", '<p><strong>Web Apps</strong> is a simple tool to manage web applications.</p><p>0.0.0.0</p><a href="https://google.com">License</a> | <a href="https://google.com">Report Bugs</a>')
        



    def on_stackedWidget_currentChanged(self, index: int):
        if index == 0:
            self.__toolbar.show()
        else:
            self.__toolbar.hide()

    def on_itemSelectionChanged(self):
        listItem = self.__listWidget.currentItem()
        if not listItem:
            self.__actionRemove.setEnabled(False)
            self.__actionEdit.setEnabled(False)
            self.__actionLaunch.setEnabled(False)
            return
        webapp = cast(WebAppLauncher, listItem.data(Qt.ItemDataRole.UserRole))
        browser = next(f for f in SUPPORTED_BROWSERS if f.name == webapp.web_browser)
        if (QIcon.hasThemeIcon(browser.icon)):
            browserIcon = QIcon.fromTheme(browser.icon)
        else:
            browserIcon = QIcon.fromTheme(XDG_APPLICATION_INTERNET)
        self.__actionLaunch.setIcon(browserIcon)
        self.__actionRemove.setEnabled(True)
        self.__actionEdit.setEnabled(True)
        self.__actionLaunch.setEnabled(True)

    selected_webapp: WebAppLauncher | None = None

    def load_webapps(self):
        # Clear treeview and selection
        self.__listWidget.clear()
        self.selected_webapp = None
        self.__actionRemove.setEnabled(False)
        self.__actionEdit.setEnabled(False)
        self.__actionLaunch.setEnabled(False)
        webapps = self.__manager.get_webapps()
        for webapp in webapps:
            if webapp.is_valid:
                if webapp.icon is not None and os.path.sep in webapp.icon and os.path.exists(webapp.icon):
                    pixmap = QPixmap(webapp.icon).scaledToHeight(int(32 * self.__ICON_Y_SCALE_FACTOR), Qt.TransformationMode.SmoothTransformation)
                    icon = QIcon(pixmap)
                elif webapp.icon is not None and QIcon.hasThemeIcon(webapp.icon):
                    icon = QIcon.fromTheme(webapp.icon)
                else:
                    icon = QIcon.fromTheme(XDG_APPLICATION_EXECUTABLE)
                item = QListWidgetItem(icon, webapp.name)
                item.setStatusTip(webapp.name + " - " + webapp.url + " - " + webapp.web_browser)
                item.setData(Qt.ItemDataRole.UserRole, webapp)
                item.setToolTip(webapp.web_browser)
                item.setText(webapp.name)
                self.__listWidget.addItem(item)

        # Select the 1st web-app
        if self.__listWidget.count() > 0:
            self.__listWidget.setCurrentItem(self.__listWidget.item(0))

