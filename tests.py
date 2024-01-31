import json
import unittest

from hooks import Hooks


DATA_DIR = "test_data"


class TestGetGoalsList(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = Hooks(data_dir=DATA_DIR).get_goals_list(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_filter(self):
        request = """{
            "filter_expression": "'no' in relationship"
        }"""
        expected = "relation develop learning structure behave safety budget wellbeing"
        self.check_case(request, expected)

    def test_filter_and_sort(self):
        request = """{
            "filter_expression": "'yes' in relationship",
            "sort_columns" : ["priority_c"]
        }"""
        expected = "relation learning develop structure behave safety ipv budget"
        self.check_case(request, expected)


class TestGetLTPActivitiesList(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = Hooks(data_dir=DATA_DIR).get_ltp_activities_list(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_filter(self):
        request = """{
            "filter_expression": "'Calm' in act_type and 17 in act_age"
        }"""
        expected = "friendly_chat reflect_positive checkin_chat"
        self.check_case(request, expected)


class TestGetModulesList(unittest.TestCase):
    def check_case(self, json_str, expected):
        request_json = json.loads(json_str)
        out = Hooks(data_dir=DATA_DIR).get_modules_list(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_filter_only(self):
        request = """{
            "goal_id_column": "goal_id_c",
            "goal_priority_column": "priority_in_goal_c",
            "goal_id": "relation",
            "filter_expression": "'female' in child_gender and 7 in age",
            "sort_columns": ["priority_in_topic"]
        }"""

        expected = " ".join(
            [
                "one_on_one_yc",
                "kind_to_myself_yc",
                "give_praise_yc",
                "talk_feelings_yc",
                "spirituality_yc",
            ]
        )
        self.check_case(request, expected)

    def test_filter_and_sort(self):
        request = """{
            "goal_id_column": "goal_id_c",
            "goal_priority_column": "priority_in_goal_c",
            "goal_id": "learning",
            "filter_expression": "'female' in child_gender and 6 in age",
            "sort_columns": ["priority_in_topic"]
        }"""

        expected = " ".join(
            [
                "language_yc",
                "reading1_4to6_yc",
                "reading2_4to6_yc",
                "maths1_4to6_yc",
                "maths2_4to6_yc",
                "engage_school_3to6_yc",
            ]
        )
        self.check_case(request, expected)

    def test_get_general_topicids(self):
        request = """{
            "goal_id_column": "goal_id_c",
            "goal_priority_column": "priority_in_goal_c",
            "goal_id": "learning"
        }"""
        request_json = json.loads(request)
        topicids = Hooks(data_dir=DATA_DIR).get_general_topicids(request_json)
        exp = ["language", "reading", "maths", "engage_school"]
        self.assertEqual(topicids, exp)


class TestGetGoalNames(unittest.TestCase):
    def test_basic(self):
        request = """{
            "column": "name_c",
            "language": "eng",
            "id": "safety"
        }"""
        expected = "Keep My Child Safe & Healthy"
        request_json = json.loads(request)
        out = Hooks(data_dir=DATA_DIR).get_goal_name(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_get_entries(self):
        request = """{
            "column": "checkin_c",
            "id": "relation"
        }"""
        expected = "relation_c"
        request_json = json.loads(request)
        out = Hooks(data_dir=DATA_DIR).get_goal_entry(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_get_entries_nested(self):
        request = """{
            "column": "name_c",
            "id": "relation"
        }"""
        expected = {
            "eng" : "Improve My Relationship with My Child",
            "zul" : "Thuthukisa Ubudlelwano Bami Nengane Yami",
            "hau" : "Kukhulisa Buhlobo Bami Nemntfwanami",
            "msa" : "",
            "zho" : "",
        }
        request_json = json.loads(request)
        out = Hooks(data_dir=DATA_DIR).get_goal_entry(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_numbered(self):
        request = """{
            "column": "name_c",
            "language": "eng",
            "ids": "safety learning develop"
        }"""
        expected = (
            "1. Keep My Child Safe & Healthy\n"
            "2. Prepare My Child for Success in School\n"
            "3. Support My Child's Development"
        )
        request_json = json.loads(request)
        out = Hooks(data_dir=DATA_DIR).get_numbered_goal_names(request_json)
        self.assertEqual(out[0]["text"], expected)


class TestGetModuleNames(unittest.TestCase):
    def test_basic(self):
        request = """{
            "column": "name",
            "language": "zul",
            "id": "take_a_pause"
        }"""
        expected = "yyy"
        request_json = json.loads(request)
        out = Hooks(data_dir=DATA_DIR).get_module_name(request_json)
        self.assertEqual(out[0]["text"], expected)

    def test_numbered(self):
        request = """{
            "column": "name",
            "language": "eng",
            "ids": "take_a_pause one_on_one_yc"
        }"""
        expected = "1. xxx\n" "2. One on One"
        request_json = json.loads(request)
        out = Hooks(data_dir=DATA_DIR).get_numbered_module_names(request_json)
        self.assertEqual(out[0]["text"], expected)
