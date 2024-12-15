from webapps_manager.common import _, APP_ID
class Category:
    def __init__(self, key, icon, description):
        self.key = key
        self.icon = icon
        self.description = description

SUPPORTED_CATEGORIES = [
    Category("WebApps", APP_ID, _("Web")),
    Category("Network", "applications-internet", _("Internet")),
    Category("Utility", "applications-utilities", _("Accessories")),
    Category("Games", "applications-games", _("Games")),
    Category("Graphics", "applications-graphics", _("Graphics")),
    Category("Office", "applications-office", _("Office")),
    Category("AudioVideo", "applications-multimedia", _("Sound & Video")),
    Category("Development", "applications-development", _("Programming")),
    Category("Education", "applications-science", _("Education")),
]