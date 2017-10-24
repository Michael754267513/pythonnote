#!/usr/bin/python
# coding:utf8

import subprocess

from saltstack.scripts.re_match_result import regex_match_error


def running_command(command):
    shell_command = '%s' % command
    try:
        result = subprocess.check_output(shell_command, stderr=subprocess.STDOUT, shell=True)

        if regex_match_error(result):
            return True
    except subprocess.CalledProcessError:
        return False


def get_md5sum(command):
    shell_command = '%s' % command
    try:
        stdout = subprocess.check_output(shell_command, stderr=subprocess.STDOUT, shell=True)
        # md5sum = stdout.strip('\n').split(' = ')[1]   # for mac
        md5sum = stdout.strip('\n').split()[0]   # for linux
        return md5sum
    except subprocess.CalledProcessError:
        return False
