#!/bin/python

import json
import uuid
import socket


_conf = {}


def generate_conf_file():
    try:
        with open("awerem.cfg", "w") as conf_file:
            _conf = {"uuid": uuid.uuid4().hex, "name": socket.gethostname()}
            json.dump(_conf, conf_file, indent=4, sort_keys=True)
    except IOError:
        print("Impossible to create awerem.cfg, exiting now")
        exit()


def _load_conf():
    global _conf
    try:
        with open("awerem.cfg") as conf_file:
            _conf = json.load(conf_file)
    except IOError:
        _generate_conf_file()


def _generate_conf_file():
    try:
        with open("awerem.cfg", "w") as conf_file:
            conf = {"uuid": uuid.uuid4().hex, "name": socket.gethostname()}
            json.dump(conf, conf_file, indent=4, sort_keys=True)
    except IOError:
        print("Impossible to create awerem.cfg, exiting now")
        exit()


def get_uuid():
    try:
        return _conf["uuid"]
    except KeyError:
        _load_conf()
        return _conf["uuid"]


def get_server_name():
    try:
        return _conf["name"]
    except KeyError:
        _load_conf()
        return _conf["name"]
