import unittest
import json
from requests import (
    get_goals_list,
    get_goal_name,
    get_module_name,
    get_modules_list,
    get_general_topicids,
)


class TestGetGoalsList(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = get_goals_list(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_filter(self):
        request = """{
            "filter_expression": "relationship != 'yes'"
        }"""
        expected = "relation develop learning structure behave safety budget wellbeing"
        self.check_case(request, expected)


class TestGetModulesList(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = get_modules_list(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_filter_only(self):
        # TODO: This filter_expression is a hack.
        request = """{
            "goal_id_column": "goal_id_c",
            "goal_priority_column": "priority_in_goal_c",
            "goal_id": "relation",
            "filter_expression": "child_gender == 'male|female' and age == '2|3| 4 | 5 | 6 | 7 | 8 | 9'",
            "sort_columns": ["priority_in_topic"]
        }"""

        expected = "one_on_one_yc kind_to_myself_yc give_praise_yc talk_feelings_yc spirituality_yc"
        self.check_case(request, expected)

    def test_get_general_topicids(self):
        request = """{
            "goal_id_column": "goal_id_c",
            "goal_priority_column": "priority_in_goal_c",
            "goal_id": "learning"
        }"""
        request_json = json.loads(request)
        topicids = get_general_topicids(request_json)
        exp = ["language", "reading", "maths", "engage_school"]
        self.assertEqual(topicids, exp)

class TestGetGoalName(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = get_goal_name(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_basic(self):
        request = """{
            "column": "name_c",
            "language": "eng",
            "goal_id": "safety"
        }"""
        expected = "Keep My Child Safe & Healthy"
        self.check_case(request, expected)


class TestGetModuleName(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = get_module_name(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_basic(self):
        request = """{
            "column": "name",
            "language": "zul",
            "goal_id": "take_a_pause"
        }"""
        expected = "yyy"
        self.check_case(request, expected)
