#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil

from conans import ConanFile, tools, Meson

class GdkPixbufConan(ConanFile):
    name = "gdk-pixbuf"
    version = "2.38.1"
    license = "LGPL-2.1"
    url = "https://github.com/bincrafters/conan-gdk-pixbuf"
    description = "An image loading library"
    homepage = "https://www.gtk.org/"
    author = "Bincrafters"
    topics = ("conan", "image", "loading", "gtk", "gnome")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "pkg_config"
    exports = "LICENSE"
    _source_subfolder = "source_subfolder"
    _autotools = None

    def requirements(self):
        self.requires("meson_installer/0.50.0@bincrafters/stable")
        self.requires("libpng/1.6.37@bincrafters/stable")
        self.requires("libtiff/4.0.9@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/GNOME/gdk-pixbuf/archive/{}.tar.gz"
        sha256 = "d9d4ee7a1b90fa28fca8f417b9eeef956479a5d1742b3cef837455ac3e58e116"
        tools.get(source_url.format(self.version), sha256=sha256)
        extrated_dir = self.name + "-" + self.version
        os.rename(extrated_dir, self._source_subfolder)

    def build(self):
        meson = Meson(self)
        defs = dict()
        defs["gir"] = False
        meson.configure(build_folder="build",
                        source_folder=self._source_subfolder, defs=defs)
        meson.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        meson = self._configure_meson()
        meson.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["m", "pthread"])
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))

