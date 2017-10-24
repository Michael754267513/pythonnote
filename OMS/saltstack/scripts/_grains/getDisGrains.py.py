#!/usr/bin/python


# import json
import subprocess


def getDiskGrains():
    '''
        return linux disk grains size
    '''

    grains = {}
    SHELL_CMD = "awk '/[s|v]d[a-z]$/ {print $NF, $(NF-1)}' /proc/partitions"
    process = subprocess.Popen(SHELL_CMD, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    for line in stdout.split('\n'):
        if line:
           grains['%s_size' % line.split()[0]] = str(int(line.split()[1]) / 1024 / 1024) + ' ' + 'GiB'
    return grains