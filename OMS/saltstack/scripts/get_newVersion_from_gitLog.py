#!/usr/bin/python
# --*-- coding: utf-8 --*--

import subprocess


def get_version(local_archive_path):
    version = []
    shell_path = '/data/deploy/OMS/saltstack/scripts'
    shell_command = "sh %s/shell/getGitVersion.sh %s | grep -v 'Already up-to-date.'" % (shell_path, local_archive_path)
    try:
        result = subprocess.Popen(shell_command, stdout=subprocess.PIPE, shell=True).communicate()[0]
        for line in result.split('\n'):
            if line:
                version = line.split()
        return version
    except subprocess.CalledProcessError:
        return False
