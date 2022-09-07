#!/usr/bin/env python3

from html import entities
import threading
import requests
import socket
import select
import json
import os
import datetime
import time


RESPONSE = b"HTTP/1.1 201 Created\n\nNotification Received"


# def path_to_cfg_file(file_name):
#     return os.path.join(ros_pkg.get_path("er_fiware_bridge"), "config/%s" % file_name)  ## Hardcoded


def remove_all_tasks(orion_url):
    url = orion_url + "ngsi-ld/v1/entities/"
    request = requests.get(url, params={"type": "Task", "limit": "800"})
    for parsed_json in request.json():
        id_task = parsed_json["id"]
        print("The task %s will be deleted." % id_task)
        resp = requests.delete(url=orion_url + "ngsi-ld/v1/entities/" + id_task)
        if resp.status_code == 204:
            print("Task %s successfully deleted !" % id_task)
        else:
            raise Exception("Error while deleting task. \n%s \n%s" % (resp.status_code, resp.text))


def remove_all_alerts(orion_url):
    url = orion_url + "ngsi-ld/v1/entities/"
    request = requests.get(url, params={"type": "https://uri.fiware.org/ns/data-models#Alert", "limit": "800"})
    for parsed_json in request.json():
        id_task = parsed_json["id"]
        print("The task %s will be deleted." % id_task)
        resp = requests.delete(url=orion_url + "ngsi-ld/v1/entities/" + id_task)
        if resp.status_code == 204:
            print("Task %s successfully deleted !" % id_task)
        else:
            raise Exception("Error while deleting task. \n%s \n%s" % (resp.status_code, resp.text))


def remove_all_alerts(orion_url):
    url = orion_url + "ngsi-ld/v1/entities/"
    request = requests.get(url, params={"type": "https://uri.fiware.org/ns/data-models#Device", "limit": "800"})
    for parsed_json in request.json():
        id_task = parsed_json["id"]
        print("The task %s will be deleted." % id_task)
        resp = requests.delete(url=orion_url + "ngsi-ld/v1/entities/" + id_task)
        if resp.status_code == 204:
            print("Task %s successfully deleted !" % id_task)
        else:
            raise Exception("Error while deleting task. \n%s \n%s" % (resp.status_code, resp.text))


def create_subscription_manifest(subscription_name, type, watchedAttributes, filter_query, sub_url, notification_content, subscription_port):
    manifest = {}
    manifest["id"] = subscription_name
    manifest["description"] = "Send notification to the test framework"
    manifest["type"] = "Subscription"
    manifest["entities"] = [{"type": type, "idPattern": ".*"}]
    if watchedAttributes is not None:
        manifest["watchedAttributes"] = watchedAttributes
    if filter_query is not None:
        manifest["q"] = filter_query
    manifest["notification"] = (
        {
            "attributes": notification_content,
            "format": "keyValues",
            "endpoint": {
                "uri": "http://%s:%s" % (sub_url, subscription_port),
                "accept": "application/json",
            },
        },
    )
    manifest["@context"] = (
        [
            "https://smartdatamodels.org/context.jsonld",
            "https://raw.githubusercontent.com/shop4cf/data-models/master/docs/shop4cfcontext.jsonld",
        ],
    )

    return manifest


def get_request(url, log_info=""):
    try:
        result = requests.get(url)
    except requests.RequestException as ex:
        raise ex
    if result.status_code != 200:
        raise Exception("Didn't get a good reply from the get request. \n Status code - %s \n Error Text - %s \n Log-Info - %s \n" % (result.status_code, result.text, log_info))
    else:
        return result.json()


def get_all_subscriptions(orion_url):
    subscription_url = orion_url + "ngsi-ld/v1/subscriptions"
    return get_request(
        subscription_url,
        "All Fiware Subscription Created",
    )


def get_all_entities(orion_url):
    entities_url = orion_url + "ngsi-ld/v1/entities&limits=1000"
    return get_request(entities_url, "All Fiware Created Entities")


def create_subscription(orion_url, subcription_name, type_query, watchedAttributes, querry_filter, endpoint, notification_content, port):
    json_manifest = json.dumps(
        create_subscription_manifest(
            subcription_name,
            type_query,
            watchedAttributes,
            querry_filter,
            endpoint,
            notification_content,
            port,
        )
    )
    subscription_url = orion_url + "ngsi-ld/v1/subscriptions"
    headers = {"Content-Type": "application/ld+json"}
    request = requests.post(subscription_url, data=json_manifest, headers=headers)
    if request.status_code != 201:
        print("Error ")
        print(request.text)
        return False

    else:
        print("Subcription %s created" % subcription_name)
    return True


def delete_subscription(orion_url, sub_name):
    subscription_url = orion_url + "ngsi-ld/v1/subscriptions"
    try:
        requests.delete(subscription_url + "/" + sub_name)
    except Exception as ex:
        print("Failure during Fiware Subcription %s deletion. Please check if everyting is correct. \n %s" % (sub_name, str(ex)))
    print("Subscription %s succefully deleted" % sub_name)


def update_entity(orion_url, entity, content):
    url = orion_url + "ngsi-ld/v1/entityOperations/update?options=update"
    for key, value in content.items():
        entity[key] = value
    json_dump = json.dumps([entity])
    headers = {"Content-Type": "application/ld+json"}
    req = requests.post(url, data=json_dump, headers=headers)
    if req.status_code != 204:
        print("Error Updating the entity. \n Status code - %s \n - Error Code %s" % (req.status_code, req.text))
    else:
        print("Updated Entity")


def create_entity(orion_url, content):
    url = orion_url + "ngsi-ld/v1/entities"
    headers = {"Content-Type": "application/ld+json"}

    req = requests.post(url, data=content, headers=headers)
    if req.status_code != 201:
        print("Error Creating the entity. \n Status code - %s \n - Error Code %s" % (req.status_code, req.text))
    else:
        print("Created Entity")


def publishEntityToFiware(orion_url="", entity_type="", content="", context=""):
    # Check if entity exist already
    url = orion_url + "ngsi-ld/v1/entities?id=" + content["id"]
    print("Requesting Entity ID : %s" % content["id"])
    request = requests.get(url, params={"type": entity_type})
    if request.status_code != 200:
        raise Exception("Error on getting update on entities. \n Status Code - %s \n Error - %s" % (request.status_code, request.text))
    else:
        r_json = request.text
        r_dict_list = json.loads(r_json)
        for entity in r_dict_list:
            if entity["id"] == content["id"]:
                update_entity(orion_url, entity, content, context)
                return
        create_entity(orion_url, content)


class FiwareSubscription(object):
    # TODO : Could be improved on registering of callback - Need to be thread safe
    # TODO : Check deletion status

    def __init__(
        self,
        orion_url="",
        name="",
        host_ip="localhost",
        port=20000,
        callback_functions=[],
    ):
        self._orion_url = orion_url
        self._sub_name = "urn:ngsi-ld:Subscription:" + name
        self._ip = host_ip
        self._port = port
        self._callback_functions = callback_functions
        self._subscription_active = False
        self._listening_thread = threading.Thread(target=self._run_listener)

    def _create_fiware_subscription(self, type_query, watchedAttributes, querry_filter, notification_content=["id"]):
        all_subscriptions = get_all_subscriptions(self._orion_url)
        for subscription in all_subscriptions:
            if subscription["id"] == self._sub_name:
                print("A subscription with the same id '%s' already registered. It will be deleted." % self._sub_name)
                self._delete_subscription()
            # Create the subscription
        create_subscription(self._orion_url, self._sub_name, type_query, watchedAttributes, querry_filter, self._ip, notification_content, self._port)

    def _create_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(("", self._port))
        self._socket.listen(1)

    def _run_listener(self):
        while not self._shutdown_flag:
            readable, _, _ = select.select([self._socket], [], [], 1.0)
            for socket in readable:
                if self._socket is socket:
                    client_socket, _ = self._socket.accept()
                    received_data = client_socket.recv(1024)
                    client_socket.sendall(RESPONSE)
                    if len(received_data) == 0:
                        client_socket.close()
                        continue
                    try:
                        for function in self._callback_functions:
                            function("{" + received_data.decode().split("{", 1)[1])
                    finally:
                        client_socket.close()
            time.sleep(0.1)
        self._socket.close()

    def connect_and_listen(self, type_querry="Task", watchedAttributes=None, querry_filter=None, notification_content=[]):
        self._create_fiware_subscription(type_querry, watchedAttributes, querry_filter, notification_content)
        self._subscription_active = True
        self._create_socket()
        self._shutdown_flag = False
        self._listening_thread.start()

    def shutdown_thread(self):
        if self._listening_thread is not None:
            self._shutdown_flag = True
            self._listening_thread.join()

    def shutdown_subscription(self):
        self.shutdown_thread()
        if self._subscription_active:
            self._delete_subscription()

    def _delete_subscription(self):
        delete_subscription(self._orion_url, self._sub_name)


def main(args=None):
    orion_url = "http://127.0.0.1:1026/"
    subscriber = FiwareSubscription(
        orion_url,
        "testing",
        "host.docker.internal",
        20001,
        [],
    )
    subscriber.connect_and_listen()
    time.sleep(2.0)
    subscriber.shutdown_subscription()


if __name__ == "__main__":
    main()
