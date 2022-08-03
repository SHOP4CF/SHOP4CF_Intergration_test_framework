from concurrent.futures import thread
from fiware_lib import create_subscription, get_all_subscriptions, get_all_entities, FiwareSubscription
from threading import Thread, Event
import time


def check_subscription_existence(orion_url, subscription_name):
    all_subs = get_all_subscriptions(orion_url)
    assert subscription_name in all_subs


def check_subscription_existence(orion_url, subscription_name):
    all_subs = get_all_subscriptions(orion_url)
    assert subscription_name not in all_subs


def check_entity_existence(orion_url, entity_id):
    get_all_entities = get_all_entities(orion_url)
    assert entity_id in get_all_entities()


def check_entity_inexistence(orion_url, entity_id):
    get_all_entities = get_all_entities(orion_url)
    assert entity_id not in get_all_entities()


def wait_for_task_existence(orion_url, entity_id, endpoint, port, timeout=5.0):
    event = Event()
    notif_receive = False
    id_check = False

    def wait_for_notif():
        while notif_receive == False:
            if event.is_set():
                break
            time.sleep(0.1)

    thread = Thread(target=wait_for_notif)

    def callback_fn(notif):
        print(notif)
        if entity_id in notif:
            id_check = True
        notif_receive = True

    sub = FiwareSubscription(orion_url, "test_sub_entity_check_%s" % entity_id, "*", endpoint, port, [callback_fn])
    sub.connect_and_listen()
    thread.start()
    thread.join(timeout)
    event.set()
    sub.shutdown_subscription()
    assert id_check == True
