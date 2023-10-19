import unittest
import json
from hooks import (
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
            "filter_expression": "'no' in relationship"
        }"""
        expected = "relation develop learning structure behave safety budget wellbeing"
        self.check_case(request, expected)


class TestGetModulesList(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = get_modules_list(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_filter_only(self):
        request = """{
            "goal_id_column": "goal_id_c",
            "goal_priority_column": "priority_in_goal_c",
            "goal_id": "relation",
            "filter_expression": "'female' in child_gender and 7 in age",
            "sort_columns": ["priority_in_topic"]
        }"""

        expected = "one_on_one_yc kind_to_myself_yc give_praise_yc talk_feelings_yc spirituality_yc"
        self.check_case(request, expected)

    def test_filter_and_sort(self):
        request = '''{
            "goal_id_column": "goal_id_c",
            "goal_priority_column": "priority_in_goal_c",
            "goal_id": "learning",
            "filter_expression": "'female' in child_gender and 6 in age",
            "sort_columns": ["priority_in_topic"]
        }'''

        expected = "language_yc reading1_4to6_yc reading2_4to6_yc maths1_4to6_yc maths2_4to6_yc engage_school_3to6_yc"
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
