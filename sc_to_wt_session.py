#! /usr/bin/python3

import os
import re
import uuid
import json


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


def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]


if __name__ == "__main__":

    path_to_sessions = (
        "/home/netzen/Study/conv_seccrt_windterm/seccrt/Sessions"
    )
    session_cfg = {
            "session.group": "",
            "session.icon": "session::square-mediumorchid",
            "session.label": "",
            "session.port": 22,
            "session.protocol": "SSH",
            "session.target": "",
            "session.uuid": "f7d37bf6-f2a4-4f0f-9e46-833a5f0f2cab",
            "ssh.sftp": False
        }

    sessions = (conv_seccrt(path_to_sessions))
    config = []

    for elements in dict_generator(sessions):
        group = ""
        cfg = session_cfg.copy()
        cfg["session.group"] = ""
        cfg["session.label"] = ""
        cfg["session.target"] = ""
        cfg["session.uuid"] = ""
        for element in elements:
            if ".ini" not in element:
                group = group + ">" + element
            elif ".ini" in element:
                cfg["session.group"] = group[1:]
                cfg["session.label"] = element[:-4]
                cfg["session.target"] = elements[-1:][0]
                cfg["session.uuid"] = str(uuid.uuid4())
        config.append(cfg)

    output_cfg = json.dumps(config, indent=4)

    with open("user.sessions", "w") as outfile:
        outfile.write(output_cfg)
