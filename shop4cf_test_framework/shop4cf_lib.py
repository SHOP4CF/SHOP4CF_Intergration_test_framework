#!/usr/bin/env python3

from sysconfig import get_path
import json
import os.path as path
import datetime
from enum import Enum


def get_current_time():
    # Get the current time
    timeNow = datetime.datetime.now()
    time_str = timeNow.strftime("%Y-%m-%dT%H:%M:%S.%f")
    time_str = time_str[:-3] + "Z"
    return time_str


def get_file(file_name):
    return path.dirname(path.abspath(__file__)) + "/json/" + file_name


def parse_path_key(full_dict, path):
    list_path = path.split(".", 1)
    current_key = list_path.pop(0)
    for key in full_dict.keys():
        if key.find(current_key) >= 0:
            if len(list_path) > 0:
                return parse_path_key(full_dict[current_key], list_path[0])
            else:
                return full_dict[current_key]


def set_value_path(full_dict, path, value):
    list_path = path.split(".", 1)
    current_key = list_path.pop(0)
    for key in full_dict.keys():
        if key.find(current_key) >= 0:
            if len(list_path) > 0:
                set_value_path(full_dict[current_key], list_path[0], value)
            else:
                full_dict[current_key] = value


def parse_path_value(value, path):
    if path == "":
        return value
    else:
        list_path = path.split(".")
        for elem in list_path:
            value = value[elem]

    return value


def get_data(_json, target_key="", path="", strict_key=False):
    for key, value in _json.items():
        if strict_key:
            if key == target_key:
                return parse_path_value(value, path)
        else:
            if key.find(target_key) >= 0:
                return parse_path_value(value, path)


class SHOP4CFSeverity(Enum):
    INFORMATIONAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class SHOP4CFData(object):
    def __init__(self):
        self._manifest = {}
        self.id = ""
        self.type = ""

    def from_json_file(self, filename):
        with open(get_file(filename)) as jsonfile:
            loaded_json = json.load(jsonfile)
        self.from_json(loaded_json)

    def from_json(self, _json):
        self._manifest = _json
        self.id = get_data(_json, "id", strict_key=True)
        self.type = get_data(_json, "type", strict_key=True)

    def to_json(self):
        self.set_data_in_dict(self.id, "id")
        self.set_data_in_dict(self.type, "type")
        return json.dumps(self._manifest)

    def set_data_in_dict(self, new_value, path):
        set_value_path(self._manifest, path, new_value)


class SHOP4CFDevice(SHOP4CFData):
    def __init__(self):
        super().__init__()
        self.controlledProperty = []

    def from_json(self, _json):
        super().from_json(_json)
        self.controlledPropery = get_data(_json, "controlledProperty", "value")

    def to_json(self):
        self.set_data_in_dict(self.controlledProperty, "controlledProperty.value")
        return super().to_json()


class SHOP4CFSensor(SHOP4CFDevice):
    def __init__(self):
        super().__init__()
        self.category = []
        self.serialNumber = ""
        self.value = ""
        self.date_value = ""
        self.deviceState = ""
        self.isSpecifiedBy = []

    def from_json(self, _json):
        super().from_json(_json)
        self.category = get_data(_json, "category", "value")
        self.serialNumber = get_data(_json, "serialNumber", "value")
        self.value = get_data(_json, "value", "value")
        self.date_value = get_data(_json, "value", "observedAt")
        self.deviceState = get_data(_json, "deviceState", "value")
        self.isSpecifiedBy = get_data(_json, "isSpecifiedBy", "value")

    def to_json(self):
        self.set_data_in_dict(self.category, "category.value")
        self.set_data_in_dict(self.serialNumber, "serialNumber.value")
        self.set_data_in_dict(self.value, "value.value")
        self.set_data_in_dict(self.deviceState, "deviceState.value")
        self.set_data_in_dict(self.isSpecifiedBy, "isSpecifiedBy.value")
        return super().to_json()


class SHOP4CFAGV(SHOP4CFDevice):
    def __init__(self):
        super().__init__()
        self.category = []
        self.batteryLevel = ""
        self.relativePosition = ""
        self.date_relativePosition = ""
        self.deviceState = ""
        self.isSpecifiedBy = []

    def from_json(self, _json):
        super().from_json(_json)
        self.category = get_data(_json, "category", "value")
        self.serialNumber = get_data(_json, "batteryLevel", "value")
        self.value = get_data(_json, "relativePosition", "value")
        self.date_value = get_data(_json, "relativePosition", "observedAt")
        self.deviceState = get_data(_json, "deviceState", "value")
        self.isSpecifiedBy = get_data(_json, "isSpecifiedBy", "value")

    def to_json(self):
        self.set_data_in_dict(self.category, "category.value")
        self.set_data_in_dict(self.batteryLevel, "batteryLevel.value")
        self.set_data_in_dict(self.relativePosition, "relativePosition.value")
        self.set_data_in_dict(self.date_relativePosition, "relativePosition.observedAt")
        self.set_data_in_dict(self.deviceState, "deviceState.value")
        self.set_data_in_dict(self.isSpecifiedBy, "isSpecifiedBy.value")
        return super().to_json()


class SHOP4CFTask(SHOP4CFData):
    def __init__(self):
        super().__init__()
        self.isDefinedBy = ""
        self.status = ""
        self.date_status = ""

    def from_json(self, _json):
        super().from_json(_json)
        self.isDefinedBy = get_data(_json, "isDefinedBy", "object")
        self.status = get_data(_json, "status", "value")
        self.date_status = get_data(_json, "status", "observedAt")

    def to_json(self):
        self.set_data_in_dict(self.isDefinedBy, "isDefinedBy.object")
        self.set_data_in_dict(self.status, "status.value")
        self.set_data_in_dict(self.date_status, "status.observedAt")
        return super().to_json()


class SHOP4CFTask(SHOP4CFData):
    def __init__(self):
        super().__init__()
        self.isDefinedBy = ""
        self.status = ""
        self.date_status = ""

    def from_json(self, _json):
        super().from_json(_json)
        self.isDefinedBy = get_data(_json, "isDefinedBy", "object")
        self.status = get_data(_json, "status", "value")
        self.date_status = get_data(_json, "status", "observedAt")

    def to_json(self):
        self.set_data_in_dict(self.isDefinedBy, "isDefinedBy.object")
        self.set_data_in_dict(self.status, "status.value")
        self.set_data_in_dict(self.date_status, "status.observedAt")
        return super().to_json()


class SHOP4CFAGVTask(SHOP4CFTask):
    def __init__(self):
        super().__init__()
        self.involves = []
        self.happensAt_source = ""
        self.happensAt_target = ""

    def get_all_involves(self, _json):

        data = get_data(_json, "involves", "value")
        if type(data, list):  # list => look for all the objects
            data_list = []
            for value in data:
                data_list.append(value["object"])
            return data_list
        else:
            return [data["object"]]

    def get_happensAtSource(self, _json):
        data = get_data(_json, "happensAt", "value")  # list or not
        if type(data, list):  # list => look for the locationFunction.value = Source
            for value in data:
                if value["locationFunction"]["value"] == "source":
                    return value["object"]
        else:
            if data["locationFunction"]["value"] == "source":
                return data["object"]
            else:
                return ""

    def get_happensAtTarget(self, _json):
        data = get_data(_json, "happensAt", "value")  # list or not
        if type(data, list):  # list => look for the locationFunction.value = Source
            for value in data:
                if value["locationFunction"]["value"] == "target":
                    return value["object"]
        else:
            if data["locationFunction"]["value"] == "target":
                return data["object"]
            else:
                return ""

    def set_all_involves(self):
        if len(self.involves) > 1:
            self._manifest["involves"]["value"] = []
            for involved_object in self.involves:
                self._manifest["involves"]["value"].append({"type": "Relationship", "object": involved_object})
        else:
            for involved_object in self.involves:
                self._manifest["involves"]["value"] = {"type": "Relationship", "object": involved_object}

    def set_happensAtSource(self):
        data = get_data(self._manifest, "happensAt", "value")  # list or not
        if type(data, list):
            for value in data:
                if value["locationFunction"]["value"] == "source":
                    value["object"] = self.happensAt_source
        else:
            if data["locationFunction"]["value"] == "source":
                data["object"] = self.happensAt_source

    def set_happensAtTarget(self):
        data = get_data(self._manifest, "happensAt", "value")  # list or not
        if type(data, list):
            for value in data:
                if value["locationFunction"]["value"] == "target":
                    value["object"] = self.happensAt_target
        else:
            if data["locationFunction"]["value"] == "target":
                data["object"] = self.happensAt_target

    def from_json(self, _json):
        super().from_json(_json)
        self.involves = self.get_all_involves(_json)
        self.happensAt_source = self.get_happensAtSource(_json)
        self.happensAt_target = self.get_happensAtTarget(_json)

    def to_json(self):
        self.set_happensAtSource()
        self.set_happensAtTarget()
        self.set_all_involves()
        return super().to_json()


class SHOP4CFArmTask(SHOP4CFTask):
    def __init__(self):
        super().__init__()
        self.involves = []
        self.workParameters = {}

    def get_all_involves(self, _json):

        data = get_data(_json, "involves", "value")
        if type(data, list):  # list => look for all the objects
            data_list = []
            for value in data:
                data_list.append(value["object"])
            return data_list
        else:
            return [data["object"]]

    def set_all_involves(self):
        if len(self.involves) > 1:
            self._manifest["involves"]["value"] = []
            for involved_object in self.involves:
                self._manifest["involves"]["value"].append({"type": "Relationship", "object": involved_object})
        else:
            for involved_object in self.involves:
                self._manifest["involves"]["value"] = {"type": "Relationship", "object": involved_object}

    def from_json(self, _json):
        super().from_json(_json)
        self.involves = self.get_all_involves(_json)
        self.workParameters = self.get_data(_json, "workParameters", "value")

    def to_json(self):
        self.set_all_involves()
        self.set_data_in_dict(self.workParameters, "workParameters.value")
        return super().to_json()


class SHOP4CFMaterial(SHOP4CFData):
    def __init__(self):
        super().__init__()
        self.state = {}
        self.state_date = ""
        self.isSpecifiedBy = []

    def get_all_specifiedBy(self, _json):
        data = get_data(_json, "isSpecifiedBy", "value")
        if type(data, list):  # list => look for all the objects
            data_list = []
            for value in data:
                data_list.append(value["object"])
            return data_list
        else:
            return [data["object"]]

    def set_all_specifiedBy(self):
        if len(self.isSpecifiedBy) > 1:
            self._manifest["isSpecifiedBy"]["value"] = []
            for object in self.specifiedBy:
                self._manifest["isSpecifiedBy"]["value"].append({"type": "Relationship", "object": object})
        else:
            for object in self.specifiedBy:
                self._manifest["isSpecifiedBy"]["value"] = {"type": "Relationship", "object": object}

    def from_json(self, _json):
        super().from_json(_json)
        self.isSpecifiedBy = self.set_all_specifiedBy(_json)
        self.state = self.get_data(_json, "state", "value")
        self.state_date = self.get_data(_json, "state", "observedAt")

    def to_json(self):
        self.set_all_specifiedBy()
        self.set_data_in_dict(self.state, "state.value")
        self.set_data_in_dict(self.state_date, "state.observedAt")
        return super().to_json()


class SHOP4CFAsset(SHOP4CFMaterial):
    def __init__(self):
        super().__init__()
        self.description = ""

    def from_json(self, _json):
        super().from_json(_json)
        self.state_date = self.get_data(_json, "description", "value")

    def to_json(self):
        self.set_data_in_dict(self.description, "description.value")
        return super().to_json()


class SHOP4CFPerson(SHOP4CFMaterial):
    def __init__(self):
        super().__init__()
        self.firstName = ""
        self.lastName = ""

    def from_json(self, _json):
        super().from_json(_json)
        self.firstName = self.get_data(_json, "firstName", "value")
        self.lastName = self.get_data(_json, "lastName", "value")

    def to_json(self):
        self.set_data_in_dict(self.firstName, "firstName.value")
        self.set_data_in_dict(self.lastName, "lastName.value")
        return super().to_json()


class SHOP4CFProcess(SHOP4CFTask):
    def __init__(self):
        super().__init__()


class SHOP4CFProcessCompose(SHOP4CFProcess):
    def __init__(self):
        super().__init__()
        self.isComposedOf = []
        self.isComposedOf_date = ""
        self.outputParameters = {}

    def get_all_isComposedOf(self, _json):
        data = get_data(_json, "isComposedOf", "value")
        if type(data, list):  # list => look for all the objects
            data_list = []
            for value in data:
                data_list.append(value["object"])
            return data_list
        else:
            return [data["object"]]

    def set_all_isComposedOf(self):
        if len(self.isComposedOf) > 1:
            self._manifest["isComposedOf"]["value"] = []
            for object in self.isComposedOf:
                self._manifest["isComposedOf"]["value"].append({"type": "Relationship", "object": object})
        else:
            for object in self.isComposedOf:
                self._manifest["isComposedOf"]["value"] = {"type": "Relationship", "object": object}

    def from_json(self, _json):
        super().from_json(_json)
        self.isComposedOf = self.get_all_isComposedOf(_json)
        self.isComposedOf_date = self.get_data(_json, "isComposedOf", "observedAt")
        self.outputParameters = self.get_data(_json, "outParameters", "value")

    def to_json(self):
        self.set_all_isComposedOf()
        self.set_data_in_dict(self.isComposedOf_date, "isComposedOf.observedAt")
        self.set_data_in_dict(self.outputParameters, "outputParameters.value")
        return super().to_json()


class SHOP4CFAlert(SHOP4CFData):
    def __init__(self):
        super().__init__()
        self.category = ""
        self.subCategory = ""
        self.validTo = ""
        self.description = ""
        self.dateIssued = ""
        self.alertSource = ""
        self.source = ""
        self.validFrom = ""
        self.severity = ""
        self.humanVerified = False
        self.location = {}

    def from_json(self, _json):
        super().from_json(_json)
        self.category = self.get_data(_json, "category", "value")
        self.subCategory = self.get_data(_json, "subCategory", "value")
        self.validTo = self.get_data(_json, "validTo", "value.@value")
        self.description = self.get_data(_json, "description", "value")
        self.location = self.get_data(_json, "location", "value")
        self.dateIssued = self.get_data(_json, "dateIssued", "value.@value")
        self.alertSource = self.get_data(_json, "alertSource", "object")
        self.source = self.get_data(_json, "source", "value")
        self.validFrom = self.get_data(_json, "validFrom", "value.@value")
        self.severity = self.get_data(_json, "severity", "value")
        self.humanVerified = self.get_data(_json, "humanVerified", "value")

    def to_json(self):
        self.set_data_in_dict(self.category, "category.value")
        self.set_data_in_dict(self.subCategory, "subCategory.value")
        self.set_data_in_dict(self.validTo, "validTo.value.@value")
        self.set_data_in_dict(self.subCategory, "subCategory.value")
        self.set_data_in_dict(self.description, "description.value")
        self.set_data_in_dict(self.location, "location.value")
        self.set_data_in_dict(self.dateIssued, "dateIssued.value.@value")
        self.set_data_in_dict(self.alertSource, "alertSource.object")
        self.set_data_in_dict(self.source, "source.value")
        self.set_data_in_dict(self.validFrom, "validFrom.value.@value")
        self.set_data_in_dict(self.severity, "severity.value")
        self.set_data_in_dict(self.humanVerified, "humanVerified.value")
        return super().to_json()
