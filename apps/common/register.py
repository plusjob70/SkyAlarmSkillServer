from __future__ import annotations
from typing import TYPE_CHECKING
from importlib import import_module

import os
import re

if TYPE_CHECKING:
    from flask import Flask


class BlueprintRegister:
    """
    module_path: from "{}.{}.{}" import ...
    controllers_name: parent(directory) name
    """
    def __init__(self, app: Flask, module_path: str, controllers_name: str):
        self.app: Flask = app
        self.module_path: str = module_path
        self.controllers_name: str = controllers_name
        self.controller_path: str = self.app.root_path
        self.directories: list[str] = []

    # ignore "__pycache__/" directories
    __ignore = staticmethod(lambda _name: True if re.match('__.*__', _name) else False)

    def __append_dir(self, path: str, name: str):
        dir_path = f'{path}/{name}'
        self.directories.append(dir_path.replace(self.controller_path, ''))
        self.__find_dir(dir_path)

    def __find_dir(self, path: str):
        for name in os.listdir(path):
            if os.path.isdir(f'{path}/{name}') and not self.__ignore(name):
                self.__append_dir(path, name)

    def register(self):
        self.__find_dir(path=self.controller_path)

        for dir_path in self.directories:
            dir_path = dir_path[1:].replace('/', '.')
            module_path = f'{self.module_path}.{dir_path}.{self.controllers_name}'
            module = import_module(module_path)
            self.app.register_blueprint(module.app)

