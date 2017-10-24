#!/usr/bin/python

import os

from saltstack.scripts.execute_command import running_command


def get_repo_url(data):
    if data.repo_protocol == '3':
        repository_url = 'https://%s:%s@%s' % (data.repo_user, data.repo_pass, data.repo_address)
    elif data.repo_protocol == '2':
        repository_url = 'http://%s:%s@%s' % (data.repo_user, data.repo_pass, data.repo_address)
    else:
        repository_url = '%s@%s' % (data.repo_user, data.repo_address)
    return repository_url


def git_checkout(source_path, project, repository_url):
    if os.path.exists(os.path.join(source_path, project)):
        command = 'cd %s && git pull' % os.path.join(source_path, project)
    else:
        command = 'git clone %s %s' % (repository_url, os.path.join(source_path, project))

    result = running_command(command)

    return result


def archive_compress(source_path, project, compress_file):
    command = 'cd %s && git archive --format zip --output %s master' % \
              (os.path.join(source_path, project), compress_file)

    if running_command(command):
        return True
