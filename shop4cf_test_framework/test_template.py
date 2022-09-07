from shop4cf_test_framework.fiware_lib import get_all_subscriptions, get_all_entities, FiwareSubscription
from threading import Thread, Event
import time
import json


def check_subscription_existence(orion_url, subscription_name):
    all_subs = get_all_subscriptions(orion_url)
    assert subscription_name in all_subs


def check_subscription_inexistence(orion_url, subscription_name):
    all_subs = get_all_subscriptions(orion_url)
    assert subscription_name not in all_subs


def check_entity_existence(orion_url, entity_id):
    get_all_entities = get_all_entities(orion_url)
    assert entity_id in get_all_entities()


def check_entity_inexistence(orion_url, entity_id):
    get_all_entities = get_all_entities(orion_url)
    assert entity_id not in get_all_entities()


def wait_for_existence(orion_url, entity_id, endpoint, port, timeout=5.0, do_something=None):
    event = Event()
    global check
    check = False

    def wait_for_notif():
        while True:
            if event.is_set():
                break
            time.sleep(0.1)

    thread = Thread(target=wait_for_notif)

    def callback_fn(notif):
        global check
        data = json.loads(notif)["data"][0]
        if data["id"].find(entity_id) >= 0:
            check = True
            event.set()

    sub = FiwareSubscription(orion_url, "test_sub_entity_check_%s" % entity_id, endpoint, port, [callback_fn])
    sub.connect_and_listen()
    thread.start()
    if do_something is not None:
        do_something()
    thread.join(timeout)
    event.set()
    sub.shutdown_subscription()
    assert check == True


if __name__ == "__main__":
    orion_url = "http://127.0.0.1:1026/"
    wait_for_existence(orion_url, "urn:ngsi-ld:Task:test:test", "host.docker.internal", 20001, timeout=5.0)
