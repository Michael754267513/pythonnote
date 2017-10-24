#!/usr/bin/python

import os
from OMS.settings import SALT_FILES_ROOT


def create_folder(folder):
    if not os.path.exists(os.path.join(SALT_FILES_ROOT, folder)):
        return os.makedirs(os.path.join(SALT_FILES_ROOT, folder))

