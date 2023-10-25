import unittest
import json

from sheets import (
    get_module_data_global_sheet,
    get_goal_module_link_global_sheet,
    get_goal_data_global_sheet,
    get_ltp_activities_sheet,
)

class TestRetrieve(unittest.TestCase):

    def test_retrieve(self):
    	get_module_data_global_sheet()
    	get_goal_module_link_global_sheet()
    	get_goal_data_global_sheet()
    	get_ltp_activities_sheet()


class TestIDValidity(unittest.TestCase):

    def test_module_IDs(self):
        module_data = get_module_data_global_sheet()
        link_data = get_goal_module_link_global_sheet()
        for ID, row in module_data.items():
            self.assertTrue(hasattr(row, "topic_ID"), row)
            self.assertTrue(hasattr(row, "name"), row)
            self.assertIn(row.topic_ID, link_data, row)
        # TODO: If we have a list of all modules in RapidPro,
        # we can also check that the module ID is from that list

    def test_ltp_headers(self):
        data = get_ltp_activities_sheet()
        for ID, row in data.items():
            self.assertTrue(hasattr(row, "name"), row)

    def test_link_IDs(self):
        link_data = get_goal_module_link_global_sheet()
        module_data = get_module_data_global_sheet()
        topic_IDs = {e.topic_ID for e in module_data.values()}
        goal_data = get_goal_data_global_sheet()
        for ID, row in link_data.items():
            self.assertIn(ID, topic_IDs, row)
            if row.goal_id_c:
                self.assertIn(row.goal_id_c, goal_data, row)
                self.assertTrue(row.priority_in_goal_c, row)
            if row.goal_id_t:
                self.assertIn(row.goal_id_t, goal_data, row)
                self.assertTrue(row.priority_in_goal_t, row)
