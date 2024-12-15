import shutil
from typing import Callable, cast
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton,QComboBox, QCheckBox, QFormLayout, QApplication, QMessageBox
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import Qt
from webapps_manager.common import ICONS_DIR, REFERENCE_DPI, WebAppLauncher, APP_ID, _
from webapps_manager.WebAppManager import WebAppManager, download_favicon, get_url_title, normalize_url
from webapps_manager.icons import XDG_APPLICATION_EXECUTABLE, XDG_APPLICATION_INTERNET
from webapps_manager.category import SUPPORTED_CATEGORIES, Category
from webapps_manager.browser import Browser,SUPPORTED_BROWSERS
import subprocess
import os
import asyncio

class WebAppEdit:
    def __init__(self, window: QWidget, editPage: QWidget, manager:WebAppManager, doneCallback: Callable[[], None]):
        self.manager = manager
        self.__ICON_X_SCALE_FACTOR = window.logicalDpiX() / REFERENCE_DPI
        self.__ICON_Y_SCALE_FACTOR = window.logicalDpiY() / REFERENCE_DPI
        self.__window = editPage

        self.__btnCancel = cast(QPushButton, editPage.findChild(QPushButton, "btnCancel"))
        self.__btnRemove = cast(QPushButton, editPage.findChild(QPushButton, "btnRemove"))
        self.__btnApply = cast(QPushButton, editPage.findChild(QPushButton, "btnApply"))

        self.__formLayout = cast(QFormLayout, editPage.findChild(QFormLayout, "formLayout"))       
        self.__txtAddress = cast(QLineEdit, editPage.findChild(QLineEdit, "txtAddress"))
        self.__actionFetch = cast(QAction, window.findChild(QAction, "actionFetch"))
        self.__actionFetch.triggered.connect(lambda: asyncio.ensure_future(self.actionFetch_clicked()))
        self.__txtAddress.addAction(self.__actionFetch, QLineEdit.ActionPosition.TrailingPosition)
        self.__txtName = cast(QLineEdit, editPage.findChild(QLineEdit, "txtName"))
        self.__lstCategory = cast(QComboBox, editPage.findChild(QComboBox, "lstCategory"))
        self.__lstCategory.clear()
        for cat in SUPPORTED_CATEGORIES:
            self.__lstCategory.addItem(QIcon.fromTheme(cat.icon), cat.description, cat)

        self.__lstBrowser = cast(QComboBox, editPage.findChild(QComboBox, "lstBrowser"))
        for browser in SUPPORTED_BROWSERS:
                if browser.exists:
                    if (QIcon.hasThemeIcon(browser.icon)):
                        browserIcon = QIcon.fromTheme(browser.icon)
                    else:
                        browserIcon = QIcon.fromTheme(XDG_APPLICATION_INTERNET)
                    self.__lstBrowser.addItem(browserIcon, browser.name, browser)
        if self.__lstBrowser.count() == 0:
            self.__lstBrowser.setToolTip("No supported browsers found")
        self.__btnIcon = cast(QPushButton, editPage.findChild(QPushButton, "btnIcon"))
        self.__txtParams = cast(QLineEdit, editPage.findChild(QLineEdit, "txtParams"))
        self.__chkIsolated = cast(QCheckBox, editPage.findChild(QCheckBox, "chkIsolated"))
        self.__chkNavBar = cast(QCheckBox, editPage.findChild(QCheckBox, "chkNavBar"))
        self.__chkIncognito = cast(QCheckBox, editPage.findChild(QCheckBox, "chkIncognito"))
        self.__doneCallback = doneCallback  

        self.__btnIcon.clicked.connect(lambda: asyncio.ensure_future(self.btnIcon_clicked()))
        self.__btnCancel.clicked.connect(self.btn_cancel_clicked)
        self.__btnRemove.clicked.connect(self.btn_remove_clicked)
        self.__btnApply.clicked.connect(self.btn_apply_clicked)

    selected_webapp: WebAppLauncher | None = None
    fetching: bool = False
    icon_file: str | None = None
    def btn_cancel_clicked(self):
        if (not self.fetching):
            self.__doneCallback()
        else:
            self.cancelFetch()
    def btn_remove_clicked(self):
        self.remove(self.selected_webapp)

    def btn_apply_clicked(self):
        category: Category = self.__lstCategory.currentData() 
        browser: Browser = self.__lstBrowser.currentData()
        name = self.__txtName.text()
        url = self.__txtAddress.text()
        isolate_profile = self.__chkIsolated.isChecked()
        navbar = self.__chkNavBar.isChecked()
        privatewindow = self.__chkIncognito.isChecked()
        custom_parameters = self.__txtParams.text()
        if self.icon_file and (os.path.sep + "tmp") in self.icon_file:
            # If the icon path is in /tmp, move it.
            filename = "".join(filter(str.isalpha, name)) + ".png"
            new_path = os.path.join(ICONS_DIR, filename)
            shutil.copyfile(self.icon_file, new_path)
            self.icon_file = new_path
        if self.selected_webapp is not None:
            self.manager.edit_webapp(self.selected_webapp.path, name, browser, url, self.icon_file, category.key, custom_parameters, self.selected_webapp.codename, isolate_profile, navbar, privatewindow)
        else:
            self.manager.create_webapp(name, url, self.icon_file, category.key, browser, custom_parameters, isolate_profile, navbar,
                                       privatewindow)
            
        self.__doneCallback()

    async def actionFetch_clicked(self):
        for i in range(self.__formLayout.count() - 1):
            self.__formLayout.itemAt(i).widget().setEnabled(False)
        self.__btnApply.setEnabled(False)
        self.__btnRemove.setEnabled(False)
        self.__btnCancel.setCursor(Qt.CursorShape.ArrowCursor)
        self.__window.setCursor(Qt.CursorShape.WaitCursor)
        self.fetching = True
        url = normalize_url(self.__txtAddress.text())
        try:
            images = await download_favicon(url)
            if len(images) > 0:
                (img, file) = images[0]
                self.icon_file = file
                self.__btnIcon.setIcon(QIcon(QPixmap(file)))
            else:
                self.icon_file = None
                self.__btnIcon.setIcon(QIcon.fromTheme(XDG_APPLICATION_EXECUTABLE))
            title = await get_url_title(url)
            self.__txtName.setText(title or self.__txtName.text())
            self.__txtAddress.setText(url)
        except Exception as e:
            self.icon_file = None
            self.__btnIcon.setIcon(QIcon.fromTheme(XDG_APPLICATION_EXECUTABLE))
            print(e)
        finally:
            self.cancelFetch()
            return

    def cancelFetch(self):
        for i in range(self.__formLayout.count() - 1):
            self.__formLayout.itemAt(i).widget().setEnabled(True)
        self.__btnApply.setEnabled(True)
        self.__btnRemove.setEnabled(True)
        self.__window.setCursor(Qt.CursorShape.ArrowCursor)
        self.__lstBrowser.setEnabled(self.selected_webapp is None)
        self.__txtAddress.setFocus()
        self.fetching = False
    
    def createNew(self):
        self.selected_webapp = None
        self.__txtAddress.clear()
        self.__txtAddress.setFocus()
        self.__txtName.clear()
        self.__lstCategory.setCurrentIndex(0)
        self.__lstBrowser.setCurrentIndex(0)
        self.__lstBrowser.setEnabled(self.selected_webapp is None)
        self.__txtParams.clear()
        self.__chkIsolated.setChecked(False)
        self.__chkNavBar.setChecked(False)
        self.__chkIncognito.setChecked(False)
        self.__btnIcon.setIcon(QIcon.fromTheme(XDG_APPLICATION_EXECUTABLE))
        self.icon_file = None
        self.__btnRemove.hide()
        self.__btnApply.setText("Create")
       
    
    def edit(self, webapp: WebAppLauncher):
        self.selected_webapp = webapp
        self.__txtAddress.setText(webapp.url)
        self.__txtAddress.setFocus()
        self.__txtName.setText(webapp.name)
        self.__lstCategory.setCurrentText(webapp.category or "")
        self.__lstBrowser.setCurrentText(webapp.web_browser or "")
        self.__lstBrowser.setEnabled(self.selected_webapp is None)
        self.__txtParams.setText(webapp.custom_parameters or "")
        self.__chkIsolated.setChecked(webapp.isolate_profile)
        self.__chkNavBar.setChecked(webapp.navbar)
        self.__chkIncognito.setChecked(webapp.privatewindow)
        self.__btnRemove.show()
        self.__btnApply.setText("Save")

        icon: QIcon | None = None
        if webapp.icon is not None and os.path.sep in webapp.icon and os.path.exists(webapp.icon):
            pixmap = QPixmap(webapp.icon).scaledToHeight(int(32 * self.__ICON_Y_SCALE_FACTOR), Qt.TransformationMode.SmoothTransformation)
            icon = QIcon(pixmap)
            self.icon_file = webapp.icon
        elif webapp.icon is not None and QIcon.hasThemeIcon(webapp.icon):
            icon = QIcon.fromTheme(webapp.icon)
            self.icon_file = webapp.icon
        else:
            icon = QIcon.fromTheme(XDG_APPLICATION_EXECUTABLE)
            self.icon_file = None
        self.__btnIcon.setIcon(icon)
        self.__btnIcon.setIconSize(icon.availableSizes()[0])
    def remove(self, webapp: WebAppLauncher | None):
        if webapp is not None:
            dialog = QMessageBox.critical(self.__window, _("Delete Web App"), _("Are you sure you want to delete '%s'?") % webapp.name, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            if dialog == QMessageBox.StandardButton.Yes:
                self.manager.delete_webbapp(webapp)
                self.__doneCallback()



    async def btnIcon_clicked(self):
        isFlatpak = os.getenv("container") == "flatpak"
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.__window.setEnabled(False)
        command = ["flatpak-spawn", "--host", "kdialog"] if isFlatpak else ["kdialog"]
        command.extend(['--desktopfile', APP_ID,'--icon', APP_ID, '--title', _('Select icon'), '--geticon'])
        #TODO: Ideally this should actually call KIconDialog or use a KIconButton from KF6, but I can't find a way to do that in PySide6
        result = await asyncio.to_thread(subprocess.run, command, stdout=subprocess.PIPE)
        icon_selected = result.stdout.decode('utf-8').removesuffix('\n')
        if icon_selected and icon_selected != "" and QIcon.hasThemeIcon(icon_selected):
            icon = QIcon.fromTheme(icon_selected)
            self.__btnIcon.setIcon(icon)
            self.icon_file = icon_selected
        if QApplication.overrideCursor():
            QApplication.restoreOverrideCursor()
        self.__window.setEnabled(True)

