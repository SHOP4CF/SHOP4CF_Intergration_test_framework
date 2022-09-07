import pytest
import shop4cf_test_framework.test_template as tt

orion_url = "http://127.0.0.1:1026/"


def check_sub_existence():
    tt.check_subscription_existence(orion_url, "ER_bridge_agv")
    tt.check_subscription_existence(orion_url, "ER_bridge_arm")


def check_task_update():
    tt.check_entity_existence(orion_url, "test_task")