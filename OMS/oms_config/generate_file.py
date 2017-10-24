#!/usr/bin/python
# -*- coding:utf-8 -*-


import re


def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


def execute_replace(replacements, file_name, target_file):
    # print replacements
    with open(file_name) as text:
        new_text = multiple_replace(replacements, text.read())
    with open(target_file, "w") as result:
        result.write(new_text)
