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
from parenttext_goals_webhooks.sheets import DataSource, JSONDataSource
import parenttext_goals_webhooks.models as models

DATA_DIR = Path(__file__).parent / "sheets"


class BaseTestCase(TestCase):
    def setUp(self):
        self.hooks = Hooks(self.datasource())

    def datasource(self):
        return DataSource(source=DATA_DIR)


class TestGetGoalsList(BaseTestCase):
    def test_filter(self):
        q = ListQuery(filter_expression="'no' in relationship")

        self.assertEqual(
            self.hooks.get_goals_list(q),
            "relation develop learning structure behave safety budget wellbeing",
        )

    def test_filter_and_sort(self):
        q = ListQuery(
            filter_expression="'yes' in relationship",
            sort_columns=["priority_c"],
        )

        self.assertEqual(
            self.hooks.get_goals_list(q),
            "relation learning develop structure behave safety ipv budget",
        )


class TestGetLTPActivitiesList(BaseTestCase):
    def test_filter(self):
        q = ListQuery(filter_expression="'Calm' in act_type and 17 in act_age")

        self.assertEqual(
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

        self.assertEqual(self.hooks.get_modules_list(q), expected)

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
        self.assertEqual(self.hooks.get_modules_list(q), expected)

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

        self.assertEqual(self.hooks.get_goal_name(q), "Keep My Child Safe & Healthy")

    def test_get_entries(self):
        q = EntryQuery(
            column="checkin_c",
            id="relation",
        )

        self.assertEqual(self.hooks.get_goal_entry(q), "relation_c")

    def test_get_entries_nested(self):
        q = EntryQuery(
            column="name_c",
            id="relation",
        )
        expected = {
            "eng": "Improve My Relationship with My Child",
            "hau": "Kukhulisa Buhlobo Bami Nemntfwanami",
            "zul": "Thuthukisa Ubudlelwano Bami Nengane Yami",
        }

        self.assertEqual(dict(sorted(self.hooks.get_goal_entry(q).items())), expected)

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

        self.assertEqual(self.hooks.get_numbered_goal_names(q), expected)


class TestGetModuleNames(BaseTestCase):
    def test_basic(self):
        q = NameQuery(
            column="name",
            language="zul",
            id="take_a_pause",
        )

        self.assertEqual(self.hooks.get_module_name(q), "yyy")

    def test_numbered(self):
        q = NumberedNamesQuery(
            column="name",
            language="eng",
            ids="take_a_pause one_on_one_yc",
        )

        self.assertEqual(
            self.hooks.get_numbered_module_names(q),
            "1. xxx\n" "2. One on One",
        )


class BaseTestHooksJSON(BaseTestCase):
    def datasource(self):
        return JSONDataSource(root=DATA_DIR)


class TestGetGoalsListJSON(BaseTestHooksJSON, TestGetGoalsList):
    pass


class TestGetGoalNamesJSON(BaseTestHooksJSON, TestGetGoalNames):
    pass


class TestGetLTPActivitiesListJSON(BaseTestHooksJSON, TestGetLTPActivitiesList):
    pass


class TestGetModuleNamesJSON(BaseTestHooksJSON, TestGetModuleNames):
    pass


class TestGetModulesListJSON(BaseTestHooksJSON, TestGetModulesList):
    pass


class TestJSONDataSource(TestCase):
    def test_load_from_json(self):
        ds = JSONDataSource(root=DATA_DIR)

        self.assertEqual(len(ds.goals()), 9)
        self.assertEqual(type(ds.goals()["relation"]), models.GoalDataGlobal)

        self.assertEqual(len(ds.goal_topic_links()), 56)
        self.assertEqual(
            type(ds.goal_topic_links()["take_a_pause"]), models.GoalModuleLinkGlobal
        )

        self.assertEqual(len(ds.ltp_activities()), 7)
        self.assertEqual(type(ds.ltp_activities()["dance_moves"]), models.LTPActivities)

        self.assertEqual(len(ds.modules()), 80)
        self.assertEqual(type(ds.modules()["take_a_pause"]), models.ModuleDataGlobal)
