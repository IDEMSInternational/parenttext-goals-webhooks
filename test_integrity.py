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


'''
TODO: Check for the following data

goal_module_link_global:
- ID: must be in module_data_global.topic_ID
- goal_id_c: must be in goal_data_global.ID
- goal_id_t: must be in goal_data_global.ID


goal_data_global:

module_data_global:
- topic_ID: must be in goal_module_link_global.ID
- ID: [in List of all modules]

ensure sheets have the right columns
'''