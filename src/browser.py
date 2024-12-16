
from enum import Enum, auto
import os
from webapps_manager.common import IS_FLATPAK
OS_BIN = "/usr/bin" if not IS_FLATPAK else "/run/host/bin"


class BrowserType(Enum):
    BROWSER_TYPE_FIREFOX=auto(),
    BROWSER_TYPE_FIREFOX_FLATPAK=auto(),
    BROWSER_TYPE_FIREFOX_SNAP=auto(),
    BROWSER_TYPE_LIBREWOLF_FLATPAK=auto(),
    BROWSER_TYPE_WATERFOX_FLATPAK=auto(),
    BROWSER_TYPE_FLOORP_FLATPAK=auto(),
    BROWSER_TYPE_CHROMIUM=auto(),
    BROWSER_TYPE_EPIPHANY=auto(),
    BROWSER_TYPE_FALKON=auto()

class Browser:

    def __init__(self, browser_type: BrowserType, name: str, exec_path: str, test_path: str, icon: str):
        self.browser_type = browser_type
        self.name = name
        self.exec_path = exec_path
        self.test_path = test_path
        self.icon = icon
        self.exists = os.path.exists(test_path) or os.path.islink(test_path)

SUPPORTED_BROWSERS = [Browser(BrowserType.BROWSER_TYPE_FIREFOX, "Firefox", "firefox", f"{OS_BIN}/firefox", "firefox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX, "Firefox Developer Edition", "firefox-developer-edition", f"{OS_BIN}/firefox-developer-edition", "firefox-developer-edition"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX, "Firefox Nightly", "firefox-nightly", f"{OS_BIN}/firefox-nightly", "firefox-nightly"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX, "Firefox Extended Support Release", "firefox-esr", f"{OS_BIN}/firefox-esr", "firefox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX_FLATPAK, "Firefox (Flatpak)", "/var/lib/flatpak/exports/bin/org.mozilla.firefox", "/var/lib/flatpak/exports/bin/org.mozilla.firefox", "firefox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX_FLATPAK, "Firefox (Flatpak)", ".local/share/flatpak/exports/bin/org.mozilla.firefox", ".local/share/flatpak/exports/bin/org.mozilla.firefox", "firefox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX_SNAP, "Firefox (Snap)", "/snap/bin/firefox", "/snap/bin/firefox", "firefox"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Brave", "brave", f"{OS_BIN}/brave", "brave"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Brave Browser", "brave-browser", f"{OS_BIN}/brave-browser", "brave"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Brave (Bin)", "brave-bin", f"{OS_BIN}/brave-bin", "brave"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chrome", "google-chrome-stable", f"{OS_BIN}/google-chrome-stable", "google-chrome"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chrome (Beta)", "google-chrome-beta", f"{OS_BIN}/google-chrome-beta", "google-chrome"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chrome (Flatpak)", "/var/lib/flatpak/exports/bin/com.google.Chrome", "/var/lib/flatpak/exports/bin/com.google.Chrome", "google-chrome"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chrome (Flatpak)", ".local/share/flatpak/exports/bin/com.google.Chrome", ".local/share/flatpak/exports/bin/com.google.Chrome", "google-chrome"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chromium", "chromium", f"{OS_BIN}/chromium", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chromium (chromium-browser)", "chromium-browser", f"{OS_BIN}/chromium-browser", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chromium (Snap)", "chromium", "/snap/bin/chromium", "chromium"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chromium (Bin)", "chromium-bin", f"{OS_BIN}/chromium-bin-browser", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Ungoogled Chromium", "ungoogled-chromium", f"{OS_BIN}/ungoogled-chromium", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_EPIPHANY, "Epiphany", "epiphany", f"{OS_BIN}/epiphany", "epiphany"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX,  "LibreWolf", "librewolf", f"{OS_BIN}/librewolf", "librewolf"),
                Browser(BrowserType.BROWSER_TYPE_LIBREWOLF_FLATPAK,  "LibreWolf (Flatpak)", "/var/lib/flatpak/exports/bin/io.gitlab.librewolf-community", "/var/lib/flatpak/exports/bin/io.gitlab.librewolf-community", "librewolf"),
                Browser(BrowserType.BROWSER_TYPE_LIBREWOLF_FLATPAK,  "LibreWolf (Flatpak)", ".local/share/flatpak/exports/bin/io.gitlab.librewolf-community", ".local/share/flatpak/exports/bin/io.gitlab.librewolf-community", "librewolf"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX,  "Waterfox", "waterfox", f"{OS_BIN}/waterfox", "waterfox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX,  "Waterfox Current", "waterfox-current", f"{OS_BIN}/waterfox-current", "waterfox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX,  "Waterfox Classic", "waterfox-classic", f"{OS_BIN}/waterfox-classic", "waterfox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX,  "Waterfox 3rd Generation", "waterfox-g3", f"{OS_BIN}/waterfox-g3", "waterfox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX,  "Waterfox 4th Generation", "waterfox-g4", f"{OS_BIN}/waterfox-g4", "waterfox"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX,  "Floorp", "floorp", f"{OS_BIN}/floorp", "floorp"),
                Browser(BrowserType.BROWSER_TYPE_WATERFOX_FLATPAK, "Waterfox (Flatpak)", "/var/lib/flatpak/exports/bin/net.waterfox.waterfox", "/var/lib/flatpak/exports/bin/net.waterfox.waterfox", "waterfox"),
                Browser(BrowserType.BROWSER_TYPE_WATERFOX_FLATPAK, "Waterfox (Flatpak)", ".local/share/flatpak/exports/bin/net.waterfox.waterfox", ".local/share/flatpak/exports/bin/net.waterfox.waterfox", "waterfox"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Vivaldi", "vivaldi-stable", f"{OS_BIN}/vivaldi-stable", "vivaldi"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Vivaldi Snapshot", "vivaldi-snapshot", f"{OS_BIN}/vivaldi-snapshot", "vivaldi"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Vivaldi (Flatpak)", "/var/lib/flatpak/exports/bin/com.vivaldi.Vivaldi", "/var/lib/flatpak/exports/bin/com.vivaldi.Vivaldi", "vivaldi"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Vivaldi (Flatpak)", ".local/share/flatpak/exports/bin/com.vivaldi.Vivaldi", ".local/share/flatpak/exports/bin/com.vivaldi.Vivaldi", "vivaldi"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Microsoft Edge", "microsoft-edge-stable", f"{OS_BIN}/microsoft-edge-stable", "microsoft-edge"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Microsoft Edge Beta", "microsoft-edge-beta", f"{OS_BIN}/microsoft-edge-beta", "microsoft-edge"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Microsoft Edge Dev", "microsoft-edge-dev", f"{OS_BIN}/microsoft-edge-dev", "microsoft-edge"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "FlashPeak Slimjet", "flashpeak-slimjet", f"{OS_BIN}/flashpeak-slimjet", "flashpeak-slimjet"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Ungoogled Chromium (Flatpak)", "/var/lib/flatpak/exports/bin/io.github.ungoogled_software.ungoogled_chromium", "/var/lib/flatpak/exports/bin/io.github.ungoogled_software.ungoogled_chromium", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Ungoogled Chromium (Flatpak)", ".local/share/flatpak/exports/bin/io.github.ungoogled_software.ungoogled_chromium", ".local/share/flatpak/exports/bin/io.github.ungoogled_software.ungoogled_chromium", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chromium (Flatpak)", "/var/lib/flatpak/exports/bin/org.chromium.Chromium", "/var/lib/flatpak/exports/bin/org.chromium.Chromium", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Chromium (Flatpak)", ".local/share/flatpak/exports/bin/org.chromium.Chromium", ".local/share/flatpak/exports/bin/org.chromium.Chromium", "org.chromium.Chromium"),
                Browser(BrowserType.BROWSER_TYPE_FALKON, "Falkon", "falkon", f"{OS_BIN}/falkon", "falkon"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Edge (Flatpak)", "/var/lib/flatpak/exports/bin/com.microsoft.Edge", "/var/lib/flatpak/exports/bin/com.microsoft.Edge", "microsoft-edge"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Edge (Flatpak)", ".local/share/flatpak/exports/bin/com.microsoft.Edge", ".local/share/flatpak/exports/bin/com.microsoft.Edge", "microsoft-edge"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Brave (Flatpak)", "/var/lib/flatpak/exports/bin/com.brave.Browser", "/var/lib/flatpak/exports/bin/com.brave.Browser", "brave"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Brave (Flatpak)", ".local/share/flatpak/exports/bin/com.brave.Browser", ".local/share/flatpak/exports/bin/com.brave.Browser", "brave"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Yandex", "yandex-browser", f"{OS_BIN}/yandex-browser", "yandex-browser"),
                Browser(BrowserType.BROWSER_TYPE_FALKON, "Falkon (Flatpak)", "/var/lib/flatpak/exports/bin/org.kde.falkon", "/var/lib/flatpak/exports/bin/org.kde.falkon", "falkon"),
                Browser(BrowserType.BROWSER_TYPE_FALKON, "Falkon (Flatpak)", ".local/share/flatpak/exports/bin/org.kde.falkon", ".local/share/flatpak/exports/bin/org.kde.falkon", "flakon"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Naver Whale", "naver-whale-stable", f"{OS_BIN}/naver-whale-stable", "naver-whale"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Yandex (Flatpak)", "/var/lib/flatpak/exports/bin/ru.yandex.Browser", "/var/lib/flatpak/exports/bin/ru.yandex.Browser", "yandex-browser"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Yandex (Flatpak)", ".local/share/flatpak/exports/bin/ru.yandex.Browser", ".local/share/flatpak/exports/bin/ru.yandex.Browser", "yandex-browser"),
                Browser(BrowserType.BROWSER_TYPE_CHROMIUM, "Thorium", "thorium-browser", f"{OS_BIN}/thorium-browser", "thorium-browser"),
                Browser(BrowserType.BROWSER_TYPE_FIREFOX, "Floorp", "floorp", f"{OS_BIN}/floorp", "floorp"),
                Browser(BrowserType.BROWSER_TYPE_FLOORP_FLATPAK, "Floorp (Flatpak)", "/var/lib/flatpak/exports/bin/one.ablaze.floorp", "/var/lib/flatpak/exports/bin/one.ablaze.floorp", "floorp"),
                Browser(BrowserType.BROWSER_TYPE_FLOORP_FLATPAK, "Floorp (Flatpak)", ".local/share/flatpak/exports/bin/one.ablaze.floorp", ".local/share/flatpak/exports/bin/one.ablaze.floorp", "floorp")
                ]
