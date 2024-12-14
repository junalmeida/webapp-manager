# This is the backend.
# It contains utility functions to load,
# save and delete webapps.
import configparser
import json
import os
from random import choice
import shutil
import string
import tempfile
import traceback
import sys
from typing import Any, Callable, Generator, List, Optional, cast
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import requests
import asyncio
from PIL import Image

from webapps_manager.browser import Browser, BrowserType
from webapps_manager.common import ICE_DIR, APPS_DIR, PROFILES_DIR, FIREFOX_PROFILES_DIR, FIREFOX_FLATPAK_PROFILES_DIR, ICONS_DIR, EPIPHANY_PROFILES_DIR, FALKON_PROFILES_DIR, FIREFOX_SNAP_PROFILES_DIR, LIBREWOLF_FLATPAK_PROFILES_DIR, FLOORP_FLATPAK_PROFILES_DIR
from webapps_manager.common import WebAppLauncher, _

class WebAppManager:

    def __init__(self):
        for directory in [ICE_DIR, APPS_DIR, PROFILES_DIR, FIREFOX_PROFILES_DIR, FIREFOX_FLATPAK_PROFILES_DIR, ICONS_DIR, EPIPHANY_PROFILES_DIR, FALKON_PROFILES_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def get_webapps(self):
        webapps: List[WebAppLauncher] = []
        for filename in os.listdir(APPS_DIR):
            if filename.lower().startswith("webapp-") and filename.endswith(".desktop"):
                path = os.path.join(APPS_DIR, filename)
                codename = filename.replace("webapp-", "").replace("WebApp-", "").replace(".desktop", "")
                if not os.path.isdir(path):
                    try:
                        webapp = WebAppLauncher(path, codename)
                        if webapp.is_valid:
                            webapps.append(webapp)
                    except Exception:
                        print("Could not create webapp for path %s" % path, sys.stderr)
                        traceback.print_exc()

        return webapps


    def delete_webbapp(self, webapp: WebAppLauncher):
        shutil.rmtree(os.path.join(FIREFOX_PROFILES_DIR, webapp.codename), ignore_errors=True)
        shutil.rmtree(os.path.join(FIREFOX_FLATPAK_PROFILES_DIR, webapp.codename), ignore_errors=True)
        shutil.rmtree(os.path.join(FIREFOX_SNAP_PROFILES_DIR, webapp.codename), ignore_errors=True)
        shutil.rmtree(os.path.join(PROFILES_DIR, webapp.codename), ignore_errors=True)
        # first remove symlinks then others
        if os.path.exists(webapp.path):
            os.remove(webapp.path)
        epiphany_orig_prof_dir=os.path.join(os.path.expanduser("~/.local/share"), "org.gnome.Epiphany.WebApp-" + webapp.codename)
        if os.path.exists(epiphany_orig_prof_dir):
            os.remove(epiphany_orig_prof_dir)
        shutil.rmtree(os.path.join(EPIPHANY_PROFILES_DIR, "org.gnome.Epiphany.WebApp-%s" % webapp.codename), ignore_errors=True)
        falkon_orig_prof_dir = os.path.join(os.path.expanduser("~/.config/falkon/profiles"), webapp.codename)
        if os.path.exists(falkon_orig_prof_dir):
            os.remove(falkon_orig_prof_dir)
        shutil.rmtree(os.path.join(FALKON_PROFILES_DIR, webapp.codename), ignore_errors=True)

    def create_webapp(self, name: str, url: str, icon: str | None, category: str, browser: Browser, custom_parameters: str, isolate_profile: bool=True, navbar:bool=False, privatewindow:bool=False):
        # Generate a 4 digit random code (to prevent name collisions, so we can define multiple launchers with the same name)
        random_code =  ''.join(choice(string.digits) for _ in range(4))
        codename = "".join(filter(str.isalpha, name)) + random_code
        path = os.path.join(APPS_DIR, "WebApp-%s.desktop" % codename)

        with open(path, 'w') as desktop_file:
            desktop_file.write("[Desktop Entry]\n")
            desktop_file.write("Version=1.0\n")
            desktop_file.write("Name=%s\n" % name)
            desktop_file.write("Comment=%s\n" % _("Web App"))

            exec_string = self.get_exec_string(browser, codename, custom_parameters, icon or "", isolate_profile, navbar,
                                               privatewindow, url)

            desktop_file.write("Exec=%s\n" % exec_string)
            desktop_file.write("Terminal=false\n")
            desktop_file.write("X-MultipleArgs=false\n")
            desktop_file.write("Type=Application\n")
            desktop_file.write("Icon=%s\n" % icon)
            desktop_file.write("Categories=GTK;%s;\n" % category)
            desktop_file.write("MimeType=text/html;text/xml;application/xhtml_xml;\n")
            desktop_file.write("StartupWMClass=WebApp-%s\n" % codename)
            desktop_file.write("StartupNotify=true\n")
            desktop_file.write("X-WebApp-Browser=%s\n" % browser.name)
            desktop_file.write("X-WebApp-URL=%s\n" % url)
            desktop_file.write("X-WebApp-CustomParameters=%s\n" % custom_parameters)
            desktop_file.write("X-WebApp-Navbar=%s\n" % bool_to_string(navbar))
            desktop_file.write("X-WebApp-PrivateWindow=%s\n" % bool_to_string(privatewindow))
            desktop_file.write("X-WebApp-Isolated=%s\n" % bool_to_string(isolate_profile))

            if browser.browser_type == BrowserType.BROWSER_TYPE_EPIPHANY:
                # Move the desktop file and create a symlink
                epiphany_profile_path = os.path.join(EPIPHANY_PROFILES_DIR, "org.gnome.Epiphany.WebApp-" + codename)
                new_path = os.path.join(epiphany_profile_path, "org.gnome.Epiphany.WebApp-%s.desktop" % codename)
                os.makedirs(epiphany_profile_path)
                os.replace(path, new_path)
                os.symlink(new_path, path)
                # copy the icon to profile directory
                new_icon=os.path.join(epiphany_profile_path, "app-icon.png")
                if icon:
                    shutil.copy(icon, new_icon)
                # required for app mode. create an empty file .app
                app_mode_file=os.path.join(epiphany_profile_path, ".app")
                with open(app_mode_file, 'w') as fp:
                    fp.write("")
                    pass

            if browser.browser_type == BrowserType.BROWSER_TYPE_FALKON:
                falkon_profile_path = os.path.join(FALKON_PROFILES_DIR, codename)
                os.makedirs(falkon_profile_path)
                # Create symlink of profile dir at ~/.config/falkon/profiles
                falkon_orig_prof_dir = os.path.join(os.path.expanduser("~/.config/falkon/profiles"), codename)
                os.symlink(falkon_profile_path, falkon_orig_prof_dir)


    def get_exec_string(self, browser: Browser, codename: str, custom_parameters: str, icon: str, isolate_profile: bool, navbar: bool, privatewindow: bool, url: str):
        if browser.browser_type in [BrowserType.BROWSER_TYPE_FIREFOX, BrowserType.BROWSER_TYPE_FIREFOX_FLATPAK, BrowserType.BROWSER_TYPE_FIREFOX_SNAP]:
            # Firefox based
            if browser.browser_type == BrowserType.BROWSER_TYPE_FIREFOX:
                firefox_profiles_dir = FIREFOX_PROFILES_DIR
            elif browser.browser_type == BrowserType.BROWSER_TYPE_FIREFOX_FLATPAK:
                firefox_profiles_dir = FIREFOX_FLATPAK_PROFILES_DIR
            else:
                firefox_profiles_dir = FIREFOX_SNAP_PROFILES_DIR
            firefox_profile_path = os.path.join(firefox_profiles_dir, codename)
            exec_string = ("sh -c 'XAPP_FORCE_GTKWINDOW_ICON=\"" + icon + "\" " + browser.exec_path +
                           " --class WebApp-" + codename +
                           " --name WebApp-" + codename +
                           " --profile " + firefox_profile_path +
                           " --no-remote")
            if privatewindow:
                exec_string += " --private-window"
            if custom_parameters:
                exec_string += " {}".format(custom_parameters)
            exec_string += " \"" + url + "\"" + "'"
            # Create a Firefox profile
            shutil.copytree('/usr/share/webapp-manager/firefox/profile', firefox_profile_path, dirs_exist_ok = True)
            if navbar:
                shutil.copy('/usr/share/webapp-manager/firefox/userChrome-with-navbar.css',
                            os.path.join(firefox_profile_path, "chrome", "userChrome.css"))
        elif browser.browser_type == BrowserType.BROWSER_TYPE_LIBREWOLF_FLATPAK:
            # LibreWolf flatpak
            firefox_profiles_dir = LIBREWOLF_FLATPAK_PROFILES_DIR
            firefox_profile_path = os.path.join(firefox_profiles_dir, codename)
            exec_string = ("sh -c 'XAPP_FORCE_GTKWINDOW_ICON=\"" + icon + "\" " + browser.exec_path +
                           " --class WebApp-" + codename +
                           " --name WebApp-" + codename +
                           " --profile " + firefox_profile_path +
                           " --no-remote")
            if privatewindow:
                exec_string += " --private-window"
            if custom_parameters:
                exec_string += " {}".format(custom_parameters)
            exec_string += " \"" + url + "\"" + "'"
            # Create a Firefox profile
            shutil.copytree('/usr/share/webapp-manager/firefox/profile', firefox_profile_path, dirs_exist_ok = True)
            if navbar:
                shutil.copy('/usr/share/webapp-manager/firefox/userChrome-with-navbar.css',
                            os.path.join(firefox_profile_path, "chrome", "userChrome.css"))
        elif browser.browser_type == BrowserType.BROWSER_TYPE_FLOORP_FLATPAK:
            # Floorp flatpak
            firefox_profiles_dir = FLOORP_FLATPAK_PROFILES_DIR
            firefox_profile_path = os.path.join(firefox_profiles_dir, codename)
            exec_string = ("sh -c 'XAPP_FORCE_GTKWINDOW_ICON=\"" + icon + "\" " + browser.exec_path +
                           " --class WebApp-" + codename +
                           " --name WebApp-" + codename +
                           " --profile " + firefox_profile_path +
                           " --no-remote")
            if privatewindow:
                exec_string += " --private-window"
            if custom_parameters:
                exec_string += " {}".format(custom_parameters)
            exec_string += " \"" + url + "\"" + "'"
            # Create a Firefox profile
            shutil.copytree('/usr/share/webapp-manager/firefox/profile', firefox_profile_path, dirs_exist_ok = True)
            if navbar:
                shutil.copy('/usr/share/webapp-manager/firefox/userChrome-with-navbar.css',
                            os.path.join(firefox_profile_path, "chrome", "userChrome.css"))
        elif browser.browser_type == BrowserType.BROWSER_TYPE_EPIPHANY:
            # Epiphany based
            epiphany_profile_path = os.path.join(EPIPHANY_PROFILES_DIR, "org.gnome.Epiphany.WebApp-" + codename)
            # Create symlink of profile dir at ~/.local/share
            epiphany_orig_prof_dir = os.path.join(os.path.expanduser("~/.local/share"),
                                                  "org.gnome.Epiphany.WebApp-" + codename)
            os.symlink(epiphany_profile_path, epiphany_orig_prof_dir)
            exec_string = browser.exec_path
            exec_string += " --application-mode "
            exec_string += " --profile=\"" + epiphany_orig_prof_dir + "\""
            exec_string += " \"" + url + "\""
            if custom_parameters:
                exec_string += " {}".format(custom_parameters)
        elif browser.browser_type == BrowserType.BROWSER_TYPE_FALKON:
            # KDE Falkon
            exec_string = browser.exec_path
            exec_string += " --wmclass=WebApp-" + codename
            if isolate_profile:
                exec_string += " --profile=" + codename
            if privatewindow:
                exec_string += " --private-browsing"
            if custom_parameters:
                exec_string += " {}".format(custom_parameters)
            exec_string += " --no-remote " + url
        else:
            # Chromium based
            if isolate_profile:
                profile_path = os.path.join(PROFILES_DIR, codename)
                exec_string = (browser.exec_path +
                               " --app=" + "\"" + url + "\"" +
                               " --class=WebApp-" + codename +
                               " --name=WebApp-" + codename +
                               " --user-data-dir=" + profile_path)
            else:
                exec_string = (browser.exec_path +
                               " --app=" + "\"" + url + "\"" +
                               " --class=WebApp-" + codename +
                               " --name=WebApp-" + codename)

            if privatewindow:
                if browser.name == "Microsoft Edge":
                    exec_string += " --inprivate"
                elif browser.name == "Microsoft Edge Beta":
                    exec_string += " --inprivate"
                elif browser.name == "Microsoft Edge Dev":
                    exec_string += " --inprivate"
                else:
                    exec_string += " --incognito"

            if custom_parameters:
                exec_string += " {}".format(custom_parameters)

        return exec_string

    def edit_webapp(self, path: str, name: str, browser: Browser, url: str, icon: str | None, category: str, custom_parameters: str, codename: str, isolate_profile: bool, navbar: bool, privatewindow: bool):
        config = configparser.RawConfigParser()
        #config.optionxform = str
        config.read(path)
        config.set("Desktop Entry", "Name", name)
        config.set("Desktop Entry", "Icon", icon)
        config.set("Desktop Entry", "Comment", _("Web App"))
        config.set("Desktop Entry", "Categories", "GTK;%s;" % category)

        try:
            # This will raise an exception on legacy apps which
            # have no X-WebApp-URL and X-WebApp-Browser

            exec_line = self.get_exec_string(browser, codename, custom_parameters, icon or "", isolate_profile, navbar, privatewindow, url)

            config.set("Desktop Entry", "Exec", exec_line)
            config.set("Desktop Entry", "X-WebApp-Browser", browser.name)
            config.set("Desktop Entry", "X-WebApp-URL", url)
            config.set("Desktop Entry", "X-WebApp-CustomParameters", custom_parameters)
            config.set("Desktop Entry", "X-WebApp-Isolated", bool_to_string(isolate_profile))
            config.set("Desktop Entry", "X-WebApp-Navbar", bool_to_string(navbar))
            config.set("Desktop Entry", "X-WebApp-PrivateWindow", bool_to_string(privatewindow))

        except:
            print("This WebApp was created with an old version of WebApp Manager. Its URL cannot be edited.")

        with open(path, 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)

def bool_to_string(boolean: bool):
    if boolean:
        return "true"
    else:
        return "false"

def normalize_url(url: str):
    (scheme, netloc, path, _, _, _) = urllib.parse.urlparse(url, "https")
    if not netloc and path:
        return urllib.parse.urlunparse((scheme, path, "", "", "", ""))
    return urllib.parse.urlunparse((scheme, netloc, path, "", "", ""))

async def download_image(root_url: str, link: str) -> Optional[Image.Image]:
    if "://" not in link:
        if link.startswith("/"):
            link = root_url + link
        else:
            link = root_url + "/" + link
    try:
        response = await asyncio.to_thread(requests.get, link, timeout=3)
        image = Image.open(BytesIO(response.content)) # type: ignore
        if image.height > 256: # type: ignore
            return image.resize((256, 256), Image.BICUBIC) # type: ignore
        return image
    except Exception as e:
        print(e)
        print(link)
        return None

def _find_link_favicon(soup: BeautifulSoup, iconformat: str):
    items = soup.find_all("link", {"rel": iconformat})
    for item in items:
        link = cast(str, item.get("href"))
        if link:
            yield link

def _find_meta_content(soup: BeautifulSoup, iconformat: str):
    item = soup.find("meta", {"name": iconformat})
    if not item:
        return
    link = cast(str, item.get("content")) # type: ignore
    if link:
        yield link

def _find_property(soup: BeautifulSoup, iconformat: str):
    items = soup.find_all("meta", {"property": iconformat})
    for item in items:
        link = cast(str, item.get("content"))
        if link:
            yield link

def _find_url(_soup: BeautifulSoup, iconformat: str):
    yield iconformat

async def get_url_title(url: str):
    url = normalize_url(url)

    try:
        response = await asyncio.to_thread(requests.get, url, timeout=3)
        if response.ok:
            soup = BeautifulSoup(response.content, "html.parser")
            meta = soup.find("meta", {"property": "og:title"}) or soup.find("meta", {"name": "og:title"})
            titlestr = cast(str, meta.get("content")) if meta else None   # type: ignore
            if not titlestr:
                title = soup.find("title")
                if title:
                    titlestr = title.text
            return titlestr
        return None
    except Exception as e:
        print(e)

async def download_favicon(url: str):
    images : List[tuple[Image.Image, str]]= []
    url = normalize_url(url)
    (scheme, netloc, _, _, _, _) = urllib.parse.urlparse(url)
    root_url = "%s://%s" % (scheme, netloc)

    # try favicon grabber first
    try:
        response = await asyncio.to_thread(requests.get, "https://favicongrabber.com/api/grab/%s?pretty=true" % netloc, timeout=3)
        if response.status_code == 200:
            source = response.content.decode("UTF-8")
            array = json.loads(source)
            for icon in array['icons']:
                image = await download_image(root_url, icon['src'])
                if image is not None:
                    t = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                    images.append((image, t.name))
                    image.save(t.name) # type: ignore
            images = sorted(images, key = lambda x: x[0].height, reverse=True) # type: ignore
            if images:
                return images
    except Exception as e:
        print(e)

    # Fallback: Check HTML and /favicon.ico
    try:
        response = await asyncio.to_thread(requests.get, url, timeout=3)
        if response.ok:
            import bs4
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            iconformats: List[tuple[str, Callable[[BeautifulSoup, str], Generator[str, Any, None]]]] = [
                ("apple-touch-icon", _find_link_favicon),
                ("shortcut icon", _find_link_favicon),
                ("icon", _find_link_favicon),
                ("msapplication-TileImage", _find_meta_content),
                ("msapplication-square310x310logo", _find_meta_content),
                ("msapplication-square150x150logo", _find_meta_content),
                ("msapplication-square70x70logo", _find_meta_content),
                ("og:image", _find_property),
                ("favicon.ico", _find_url),
            ]

            # icons defined in the HTML
            for (iconformat, getter) in iconformats:
                for link in getter(soup, iconformat):
                    image = await download_image(root_url, link)
                    if image is not None:
                        t = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                        images.append((image, t.name))
                        image.save(t.name) # type: ignore

    except Exception as e:
        print(e)

    images = sorted(images, key = lambda x: x[0].height, reverse=True) # type: ignore
    return images


