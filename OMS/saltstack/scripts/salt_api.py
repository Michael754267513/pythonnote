# -*- coding:utf-8 -*-

from OMS.settings import salt_api_user, salt_api_url, salt_api_password
# import json
import requests
import yaml
import os
# import urllib3


requests.packages.urllib3.disable_warnings()
# urllib3.disable_warnings()


class SaltApi:
    """
    init
    """

    def __init__(self, **kwargs):
        self.data = kwargs
        self.url = salt_api_url
        self.token = ''
        self.headers = {
            'User-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Accept': 'application/x-yaml',
        }
        s = {'expr_form': 'list', 'client': 'local'}
        self.data.update(s)

    def get_token(self):
        url = self.url + 'login'
        auth = {'username': salt_api_user,
                'password': salt_api_password,
                'eauth': 'pam'}

        self.data.update(auth)
        req = requests.post(url=url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        tmp = yaml.load(context)
        # self.token = tmp['return'][0]['token']  // for json
        self.token = tmp['return'][0]['token']
        # print self.token
        return self.token

    def get_header(self):
        header_token = {
            'X-Auth-Token': self.token
        }
        self.headers.update(header_token)
        return self.headers

    def get_no_token_heard(self):
        return self.headers


def wildcard_params(func):
    def _wildcard_params(headers, **kwargs):
        if kwargs.get('tgt') == 'all' or kwargs.get('tgt') == '':
            kwargs['tgt'] = '*'
        if kwargs.get('arg', '') == '':
            kwargs['arg'] = None
        if kwargs.get('enc', '') == '':
            kwargs['enc'] = None
        return func(headers, **kwargs)
    return _wildcard_params


def wildcard_service(func):
    def _wildcard_service(headers, **kwargs):
        if kwargs.get('tgt') == 'all' or kwargs.get('tgt') == '':
            kwargs['tgt'] = '*'
        if kwargs.get('arg', '') == '':
            kwargs['arg'] = None
        return func(headers, **kwargs)
    return _wildcard_service


@wildcard_params
def execute_command(headers, **kwargs):
    r = requests.post(url=salt_api_url, headers=headers, data=kwargs, verify=False)
    context = r.text
    # print yaml.load(context)['return'][0]
    return yaml.load(context)['return'][0]
    # return context


@wildcard_params
def users_process(headers, **kwargs):
    r = requests.post(url=salt_api_url, headers=headers, data=kwargs, verify=False)
    context = r.text
    return yaml.load(context)['return'][0]


@wildcard_params
def reset_service(headers, **data):
    url = salt_api_url + 'hook/services/restart'
    auth = {'username': salt_api_user,
            'password': salt_api_password,
            'eauth': 'pam'
            }
    data.update(auth)
    req = requests.post(url=url, headers=headers, data=data, verify=False)
    context = str(req.text).split(': ')[1]
    return context


@wildcard_service
def process(headers, **kwargs):
    r = requests.post(url=salt_api_url, headers=headers, data=kwargs, verify=False)
    context = r.text
    return context


@wildcard_service
def key_manager(headers, **kwargs):
    r = requests.post(url=salt_api_url, headers=headers, data=kwargs, verify=False)
    context = r.text
    return yaml.load(context)['return'][0]


@wildcard_params
def user_add(headers, **data):
    req = requests.post(url=salt_api_url, headers=headers, data=data, verify=False)
    context = req.text
    return context


def get_grains_items(headers, minion):
    grains_url = os.path.join(salt_api_url, 'minions', minion)
    print grains_url
    req = requests.get(url=grains_url, headers=headers, verify=False)
    context = req.text
    return yaml.load(context)['return'][0]


@wildcard_service
def set_sys_pass(headers, **data):
    url = salt_api_url + 'hook/cmd/run'
    auth = {'username': salt_api_user,
            'password': salt_api_password,
            'eauth': 'pam'
            }
    data.update(auth)
    req = requests.post(url=url, headers=headers, data=data, verify=False)
    context = str(req.text.split(': ')[1])
    return context


@wildcard_service
def change_password(headers, **kwargs):
    r = requests.post(url=salt_api_url, headers=headers, data=kwargs, verify=False)
    context = r.text
    return yaml.load(context)['return'][0]


@wildcard_service
def process_return_yaml(headers, **kwargs):
    r = requests.post(url=salt_api_url, headers=headers, data=kwargs, verify=False)
    context = r.text
    return yaml.load(context)['return'][0]
