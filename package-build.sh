#!/bin/bash
flatpak-builder -v --ccache --force-clean --install-deps-from flathub --state-dir=.flatpak/flatpak-builder .flatpak/repo ./io.github.junalmeida.webapps_manager.json
#flatpak build --share=network --filesystem=./ --filesystem=.flatpak/repo --env=LD_LIBRARY_PATH=/app/lib --env=PKG_CONFIG_PATH=/app/lib/pkgconfig:/app/share/pkgconfig:/usr/lib/pkgconfig:/usr/share/pkgconfig .flatpak/repo python -m pip install --no-build-isolation --prefix=/app .
