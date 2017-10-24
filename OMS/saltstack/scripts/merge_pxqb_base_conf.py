#!/usr/bin/python


import re


def merge_all_server(file_list, merge_name):
    merge_file = '/srv/salt/merge_config/%s/pxqb_base/config/conf.allserver.php' % merge_name
    for file_name in file_list:
        with open(merge_file, 'r') as readfile:
            content = readfile.read()
            readfile.close()
        pos = content.find(");")
        if pos != -1:
            with open(file_name) as fp:
                for result in re.findall('return array\((.*?)\);', fp.read(), re.S):
                    with open(merge_file, 'w+') as outfile:
                        outfile.write(content[:pos] + result + content[pos:])


def do_copy_new_file(source_file, merge_name):
    merge_file = '/srv/salt/merge_config/%s/pxqb_base/config/conf.allserver.php' % merge_name
    with open(source_file, 'r') as readfile:
        content = readfile.read()
        readfile.close()

    with open(merge_file, 'w') as outfile:
        outfile.write(content)
        outfile.close()

