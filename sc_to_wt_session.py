#! /usr/bin/python3

import os
import re
from pprint import pprint


path_to_sessions = "/home/netzen/Study/conv_seccrt_windterm/seccrt/tmp"


def conv_seccrt(path):
    if os.path.isdir(path):
        d = {}
        for file in os.listdir(path):
            if not file.startswith("__"):
                d[file] = conv_seccrt(os.path.join(path, file))
    else:
        with open(path, 'r') as file:
            data = file.read().rstrip()
        d = re.findall(r'S:"Hostname"=(\d+\.\d+\.\d+\.\d+)', data)
    return d


# conv_seccrt(path_to_sessions)
sessions = (conv_seccrt(path_to_sessions))

for key, value in sessions.items():
    print(key, value)
