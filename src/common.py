import gettext
import locale
import os

# i18n
APP_ID="io.github.junalmeida.webapps_manager"
APP = 'webapps_manager'
LOCALE_DIR = "/usr/share/locale"
REFERENCE_DPI = 96

locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# Constants
ICE_DIR = os.path.expanduser("~/.local/share/ice")
APPS_DIR = os.path.expanduser("~/.local/share/applications")
PROFILES_DIR = os.path.join(ICE_DIR, "profiles")
FIREFOX_PROFILES_DIR = os.path.join(ICE_DIR, "firefox")
FIREFOX_FLATPAK_PROFILES_DIR = os.path.expanduser("~/.var/app/org.mozilla.firefox/data/ice/firefox")
FIREFOX_SNAP_PROFILES_DIR = os.path.expanduser("~/snap/firefox/common/.mozilla/firefox")
LIBREWOLF_FLATPAK_PROFILES_DIR = os.path.expanduser("~/.var/app/io.gitlab.librewolf-community/data/ice/librewolf")
WATERFOX_FLATPAK_PROFILES_DIR = os.path.expanduser("~/.var/app/net.waterfox.waterfox/data")
FLOORP_FLATPAK_PROFILES_DIR = os.path.expanduser("~/.var/app/one.ablaze.floorp/data")
EPIPHANY_PROFILES_DIR = os.path.join(ICE_DIR, "epiphany")
FALKON_PROFILES_DIR = os.path.join(ICE_DIR, "falkon")
ICONS_DIR = os.path.join(ICE_DIR, "icons")

# This is a data structure representing
# the app menu item (path, name, icon..etc.)
class WebAppLauncher:

    def __init__(self, path: str, codename: str):
        self.path = path
        self.codename = codename
        self.web_browser = ""
        self.name = ""
        self.icon = None
        self.is_valid = False
        self.exec = None
        self.category = None
        self.url = ""
        self.custom_parameters = ""
        self.isolate_profile = False
        self.navbar = False
        self.privatewindow = False

        is_webapp = False
        with open(path) as desktop_file:
            for line in desktop_file:
                line = line.strip()

                # Identify if the app is a webapp
                if "StartupWMClass=WebApp" in line or "StartupWMClass=Chromium" in line or "StartupWMClass=ICE-SSB" in line:
                    is_webapp = True
                    continue

                if "Name=" in line:
                    self.name = line.replace("Name=", "")
                    continue

                if "Icon=" in line:
                    self.icon = line.replace("Icon=", "")
                    continue

                if "Exec=" in line:
                    self.exec = line.replace("Exec=", "")
                    continue

                if "Categories=" in line:
                    self.category = line.replace("Categories=", "").replace("GTK;", "").replace(";", "")
                    continue

                if "X-WebApp-Browser=" in line:
                    self.web_browser = line.replace("X-WebApp-Browser=", "")
                    continue

                if "X-WebApp-URL=" in line:
                    self.url = line.replace("X-WebApp-URL=", "")
                    continue

                if "X-WebApp-CustomParameters" in line:
                    self.custom_parameters = line.replace("X-WebApp-CustomParameters=", "")
                    continue

                if "X-WebApp-Isolated" in line:
                    self.isolate_profile = line.replace("X-WebApp-Isolated=", "").lower() == "true"
                    continue

                if "X-WebApp-Navbar" in line:
                    self.navbar = line.replace("X-WebApp-Navbar=", "").lower() == "true"
                    continue

                if "X-WebApp-PrivateWindow" in line:
                    self.privatewindow = line.replace("X-WebApp-PrivateWindow=", "").lower() == "true"
                    continue

        if is_webapp and self.name and self.web_browser and self.icon is not None:
            self.is_valid = True

