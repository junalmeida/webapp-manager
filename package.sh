#!/bin/bash

#wget https://raw.githubusercontent.com/flatpak/flatpak-builder-tools/master/pip/flatpak-pip-generator --directory-prefix .venv/bin
#python3 -m pip install requirements-parser
#python3 env/bin/flatpak-pip-generator deps


FLATPAK_REPO=webapps_manager
FLATPAK_ID=io.github.junalmeida.webapps-manager
FLATPAK_FILE=$FLATPAK_ID.json
FLATPAK_BUILD=build/flatpak

flatpak-builder --force-clean --install-deps-from flathub $FLATPAK_BUILD $FLATPAK_ID.json && \
flatpak-builder --repo $FLATPAK_REPO --ccache $FLATPAK_BUILD $FLATPAK_ID.json && \
flatpak build-bundle $FLATPAK_REPO $FLATPAK_ID.flatpak $FLATPAK_ID