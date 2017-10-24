#!/usr/bin/python
# --*-- coding: utf8 --*--


# import re
#
# regex_list = [
#     "E[R|r]{2}[O|o][R|r]",
#     "E[R|r]{2}n[O|o]",
#     "[F|f][A|a][I|i][L|l][E|e][D|d]",
#     "Failed",
#     "No such file or directory",
#     "[F|f]alse",
# ]
#
# info = "No such file or directory"
#
#
# def search_error(message):
#     try:
#         result = re.search("E[R|r]{2}[O|o][R|r]", message).group()
#     except AttributeError:
#         result = None
#
#     return result
#
#
# def search_errno(message):
#     try:
#         result = re.search("E[R|r]{2}n[O|o]", message).group()
#     except AttributeError:
#         result = None
#
#     return result
#
#
# def search_failed(message):
#     try:
#         result = re.search("[F|f][A|a][I|i][L|l][E|e][D|d]", message).group()
#     except AttributeError:
#         result = None
#
#     return result
#
#
# def search_no_file(message):
#     try:
#         result = re.search("No such file or directory", message).group()
#     except AttributeError:
#         result = None
#
#     return result
#
#
# def search_false(message):
#     try:
#         result = re.search("[F|f]alse", message).group()
#     except AttributeError:
#         result = None
#
#     return result
#
#
# def regex_match_error(message):
#     result_list = []
#     print message
#     for regex in regex_list:
#         print regex
#         try:
#             result = re.search(regex, message).group()
#             print result
#             # if result:
#             #     print result
#             #     result_list.append(result)
#         # if result_list:
#         #     return False
#         # except AttributeError:
#         #     return True
#
#
# print regex_match_error(info)

import re

regex_list = [
    "[E|e][R|r]{2}[O|o][R|r]",
    "E[R|r]{2}n[O|o]",
    "[F|f][A|a][I|i][L|l][E|e][D|d]",
    "No such file or directory",
    "[F|f]alse",
    "not available.",
]


def regex_match_error(message):
    result_list = []
    for regex in regex_list:
        try:
            result = re.search(regex, message).group()
            result_list.append(result)
        except AttributeError:
            pass

    if result_list:
        return False
    else:
        return True
