#!/bin/bash
FLATPAK_BUILD=build/flatpak
flatpak-builder --env=XDG_SESSION_TYPE=$XDG_SESSION_TYPE --run $FLATPAK_BUILD io.github.junalmeida.webapps_manager.json webapps_manager
