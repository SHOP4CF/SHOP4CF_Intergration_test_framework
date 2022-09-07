from fiware_lib import get_all_entities, create_entity, update_entity, remove_all_tasks, remove_all_alerts
from shop4cf_lib import SHOP4CFAGVTask, SHOP4CFTask
import time

if __name__ == "__main__":
    orion_url = "http://127.0.0.1:1026/"
    remove_all_tasks(orion_url)
    task = SHOP4CFTask()
    task.from_json_file("task.json")
    create_entity(orion_url, task.to_json())

    time.sleep(10.0)
