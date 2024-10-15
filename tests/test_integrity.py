from unittest import TestCase, skip

from parenttext_goals_webhooks.sheets import DataSource


@skip("Should be a validator in main app")
class TestRetrieve(TestCase):
    def test_retrieve(self):
        db = DataSource()
        self.assertGreater(len(db.goal_topic_links()), 0)
        self.assertGreater(len(db.goals()), 0)
        self.assertGreater(len(db.ltp_activities()), 0)
        self.assertGreater(len(db.modules()), 0)


@skip("Should be a validator in main app")
class TestIDValidity(TestCase):
    def setUp(self):
        self.db = DataSource()

    def test_module_IDs(self):
        module_data = self.db.modules()
        link_data = self.db.goal_topic_links()

        for ID, row in module_data.items():
            self.assertTrue(hasattr(row, "topic_ID"), row)
            self.assertTrue(hasattr(row, "name"), row)
            self.assertIn(row.topic_ID, link_data, row)

    def test_ltp_headers(self):
        data = self.db.ltp_activities()

        for ID, row in data.items():
            self.assertTrue(hasattr(row, "name"), row)

    def test_link_IDs(self):
        link_data = self.db.goal_topic_links()
        module_data = self.db.modules()
        topic_IDs = {e.topic_ID for e in module_data.values()}
        goal_data = self.db.goals()

        for ID, row in link_data.items():
            self.assertIn(ID, topic_IDs, row)
            if row.goal_id_c:
                self.assertIn(row.goal_id_c, goal_data, row)
                self.assertTrue(row.priority_in_goal_c, row)
            if row.goal_id_t:
                self.assertIn(row.goal_id_t, goal_data, row)
                self.assertTrue(row.priority_in_goal_t, row)
