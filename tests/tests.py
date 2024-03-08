from pathlib import Path
from unittest import TestCase

from parenttext_goals_webhooks.hooks import Hooks
from parenttext_goals_webhooks.main import (
    EntryQuery,
    ListQuery,
    ModulesListQuery,
    NameQuery,
    NumberedNamesQuery,
)

DATA_DIR = Path(__file__).parent / "sheets"


class BaseTestCase(TestCase):
    def setUp(self):
        self.hooks = Hooks(data_dir=DATA_DIR)

    def assertTextEqual(self, actual, expected):
        self.assertEqual(
            actual[0]["text"],
            expected,
        )


class TestGetGoalsList(BaseTestCase):
    def test_filter(self):
        q = ListQuery(filter_expression="'no' in relationship")

        self.assertTextEqual(
            self.hooks.get_goals_list(q),
            "relation develop learning structure behave safety budget wellbeing",
        )

    def test_filter_and_sort(self):
        q = ListQuery(
            filter_expression="'yes' in relationship",
            sort_columns=["priority_c"],
        )

        self.assertTextEqual(
            self.hooks.get_goals_list(q),
            "relation learning develop structure behave safety ipv budget",
        )


class TestGetLTPActivitiesList(BaseTestCase):
    def test_filter(self):
        q = ListQuery(filter_expression="'Calm' in act_type and 17 in act_age")

        self.assertTextEqual(
            self.hooks.get_ltp_activities_list(q),
            "friendly_chat reflect_positive checkin_chat",
        )


class TestGetModulesList(BaseTestCase):
    def test_filter_only(self):
        q = ModulesListQuery(
            goal_id_column="goal_id_c",
            goal_priority_column="priority_in_goal_c",
            goal_id="relation",
            filter_expression="'female' in child_gender and 7 in age",
            sort_columns=["priority_in_topic"],
        )
        expected = " ".join(
            [
                "one_on_one_yc",
                "kind_to_myself_yc",
                "give_praise_yc",
                "talk_feelings_yc",
                "spirituality_yc",
            ]
        )

        self.assertTextEqual(self.hooks.get_modules_list(q), expected)

    def test_filter_and_sort(self):
        q = ModulesListQuery(
            goal_id_column="goal_id_c",
            goal_priority_column="priority_in_goal_c",
            goal_id="learning",
            filter_expression="'female' in child_gender and 6 in age",
            sort_columns=["priority_in_topic"],
        )
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
        self.assertTextEqual(self.hooks.get_modules_list(q), expected)

    def test_get_general_topicids(self):
        q = ModulesListQuery(
            goal_id_column="goal_id_c",
            goal_priority_column="priority_in_goal_c",
            goal_id="learning",
        )
        self.assertEqual(
            self.hooks.get_general_topicids(q),
            ["language", "reading", "maths", "engage_school"],
        )


class TestGetGoalNames(BaseTestCase):
    def test_basic(self):
        q = NameQuery(
            column="name_c",
            language="eng",
            id="safety",
        )

        self.assertTextEqual(
            self.hooks.get_goal_name(q), "Keep My Child Safe & Healthy"
        )

    def test_get_entries(self):
        q = EntryQuery(
            column="checkin_c",
            id="relation",
        )

        self.assertTextEqual(self.hooks.get_goal_entry(q), "relation_c")

    def test_get_entries_nested(self):
        q = EntryQuery(
            column="name_c",
            id="relation",
        )
        expected = {
            "eng": "Improve My Relationship with My Child",
            "zul": "Thuthukisa Ubudlelwano Bami Nengane Yami",
            "hau": "Kukhulisa Buhlobo Bami Nemntfwanami",
            "msa": "",
            "spa": "",
            "zho": "",
        }

        self.assertTextEqual(self.hooks.get_goal_entry(q), expected)

    def test_numbered(self):
        q = NumberedNamesQuery(
            column="name_c",
            language="eng",
            ids="safety learning develop",
        )
        expected = (
            "1. Keep My Child Safe & Healthy\n"
            "2. Prepare My Child for Success in School\n"
            "3. Support My Child's Development"
        )

        self.assertTextEqual(self.hooks.get_numbered_goal_names(q), expected)


class TestGetModuleNames(BaseTestCase):
    def test_basic(self):
        q = NameQuery(
            column="name",
            language="zul",
            id="take_a_pause",
        )

        self.assertTextEqual(self.hooks.get_module_name(q), "yyy")

    def test_numbered(self):
        q = NumberedNamesQuery(
            column="name",
            language="eng",
            ids="take_a_pause one_on_one_yc",
        )

        self.assertTextEqual(
            self.hooks.get_numbered_module_names(q),
            "1. xxx\n" "2. One on One",
        )
