#!/bin/bash
python -m venv .venv --system-site-packages
source .venv/bin/activate
if [ ! -e "./.venv/bin/flatpak-pip-generator" ]; then
    wget https://raw.githubusercontent.com/flatpak/flatpak-builder-tools/master/pip/flatpak-pip-generator --directory-prefix .venv/bin
    chmod a+x .venv/bin/flatpak-pip-generator
fi
#dev dependencies
python -m pip install --upgrade pip
python -m pip install --upgrade requirements-parser build

#local app
python -m pip install -e . --config-settings editable_mode=strict