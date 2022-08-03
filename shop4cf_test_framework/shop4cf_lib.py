#!/usr/bin/env python3

from sysconfig import get_path
import threading
import requests
import socket
import select
import json
import os.path as path
import datetime


def get_current_time():
    # Get the current time
    timeNow = datetime.datetime.now()
    time_str = timeNow.strftime("%Y-%m-%dT%H:%M:%S.%f")
    time_str = time_str[:-3] + "Z"
    return time_str


def get_file(file_name):
    return path.dirname(path.abspath(__file__)) + "/json/" + file_name


class SHOP4CFTask(object):
    def __init__(self):
        self._manifest = {}
        self._task_id = ""
        self._involved_id = ""
        self._status = ""

    def from_config_file(self, filename):
        with open(get_path(filename)) as jsonfile:
            loaded_json = json.load(jsonfile)
        self.from_json(loaded_json)

    def from_json(self, _json):
        self._manifest = _json
        for key, value in _json.items():
            if key == "id":
                self._task_id = value

            elif key.find("involves") >= 0:
                if type(value) is not list:
                    self._involved_id = value["value"]["object"]  ## Note : Hardcoded for only 1 participant
                else:
                    for id in value:
                        self._involved_id.append(id["value"]["object"])

            elif key.find("status") >= 0:
                self._status = value["value"]

    def to_json(self):

        for key, value in self._manifest.items():
            if key == "id":
                self._manifest[key] = self._task_id

            elif key.find("involves") >= 0:
                self._manifest[key]["value"]["object"] = self._involved_id  ## Hardcoded to only one participant
            elif key.find("status") >= 0:
                self._manifest[key]["value"] = self._status
                self._manifest[key]["observedAt"] = get_current_time()


class SHOP4CFAGVFiwareTask(SHOP4CFTask):
    def __init__(self):
        super(SHOP4CFAGVFiwareTask, self).__init__()
        self._location = ""

    def from_json(self, _json):
        self._manifest = _json
        for key, value in _json.items():
            if key == "id":
                self._task_id = value

            elif key.find("happensAt") >= 0:
                if type(value["value"]) is list:
                    for elem in value["value"]:
                        if elem["locationFunction"]["value"] == "target":
                            self._location = elem["object"]
                else:
                    self._location = value["value"]["object"]

            elif key.find("involves") >= 0:
                self._involved_id = value["value"]["object"]  ## Note : Hardcoded for only 1 participant

            elif key.find("status") >= 0:
                self._status = value["value"]

    def from_config_file(self, filename):
        with open(get_path(filename)) as jsonfile:
            loaded_json = json.load(jsonfile)
        self.from_json(loaded_json)

    def to_json(self):

        for key, value in self._manifest.items():
            if key == "id":
                self._manifest[key] = self._task_id

            elif key.find("happensAt") >= 0:
                if type(value["value"]) is list:
                    for id_elem, elem in enumerate(value["value"]):
                        if elem["locationFunction"]["value"] == "target":
                            self._manifest[key]["value"][id_elem]["object"] = self._location
                else:
                    self._manifest[key]["value"]["object"] = self._location

            elif key.find("involves") >= 0:
                self._manifest[key]["value"]["object"] = self._involved_id  ## Hardcoded to only one participant
            elif key.find("status") >= 0:
                self._manifest[key]["value"] = self._status
                self._manifest[key]["observedAt"] = get_current_time()

        return self._manifest

    def set_params(self, task_id=None, location=None, involves=None, status=None):
        if task_id:
            self._task_id = task_id
        if location:
            self._location = location
        if involves:
            self._involved_id = involves
        if status:
            self._status = status

    def __eq__(self, __o):
        print(__o._task_id, self._task_id)
        if __o._task_id == self._task_id and self._involved_id == __o._involved_id:
            return True
        else:
            return False


class SHOP4CFArmFiwareTask(object):
    def __init__(self):
        self._task_id = ""
        self._defined_by = ""
        self._involved_id = ""
        self._status = ""
        self._tray_type = ""
        self._height = ""
        self._ls = ""
        self._manifest = {}

    def from_json(self, _json):
        self._manifest = _json
        for key, value in _json.items():
            if key == "id":
                self._task_id = value

            elif key.find("isDefinedBy") >= 0:
                self._defined_by = value["object"]

            elif key.find("involves") >= 0:
                self._involved_id = value["value"]["object"]  ## Note : Hardcoded for only 1 participant

            elif key.find("status") >= 0:
                self._status = value["value"]
            elif key.find("workParameters") >= 0:
                if "tray_type" in value["value"]:
                    self._tray_type = value["value"]["tray_type"]
                if "height" in value["value"]:
                    self._height = value["value"]["height"]
                if "LS" in value["value"]:
                    self._ls = value["value"]["LS"]

    def from_config_file(self, filename):
        with open(get_file(filename)) as jsonfile:
            loaded_json = json.load(jsonfile)
        self.from_json(loaded_json)

    def to_json(self):

        for key, value in self._manifest.items():
            if key == "id":
                self._manifest[key] = self._task_id

            elif key.find("isDefinedBy") >= 0:
                self._manifest[key]["object"] = self._defined_by

            elif key.find("involves") >= 0:
                self._manifest[key]["value"]["object"] = self._involved_id  ## Hardcoded to only one participant
            elif key.find("status") >= 0:
                self._manifest[key]["value"] = self._status
                self._manifest[key]["observedAt"] = get_current_time()

        return self._manifest

    def set_params(
        self,
        task_id=None,
        defined_by=None,
        involves=None,
        status=None,
    ):
        if task_id:
            self._task_id = task_id
        if defined_by:
            self._defined_by = defined_by
        if involves:
            self._involved_id = involves
        if status:
            self._status = status

    def __eq__(self, __o):
        print(__o._task_id, self._task_id)
        if __o._task_id == self._task_id and self._involved_id == __o._involved_id:
            return True
        else:
            return False

        if task_id:
            self._task_id = task_id
        if defined_by:
            self._defined_by = defined_by
        if involves:
            self._involved_id = involves
        if status:
            self._status = status

    def __eq__(self, __o):
        print(__o._task_id, self._task_id)
        if __o._task_id == self._task_id and self._involved_id == __o._involved_id:
            return True
        else:
            return False
