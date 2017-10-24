#!/usr/bin/python

import shutil
import errno
# import os


def do_copy(src, dst):
    try:
        # if os.path.exists(dst):
        #     shutil.copyfile(src, dst)
        # else:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise
