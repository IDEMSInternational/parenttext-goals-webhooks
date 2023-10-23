'''
This is a simple script for manually testing that the webhook
actually works.

The actual functionality of the webhooks is covered by the
automated tests.
'''

import requests
import json

def run_test(path, request):
    baseurl = "https://europe-west2-glossy-attic-237012.cloudfunctions.net/parenttext-individualize-module-list"
    url = baseurl + '/' + path
    data = json.loads(request)
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Success: {path}")
        print(response.json())
    elif response.status_code == 404:
        print(f"Failure with {response.status_code}: {path}")
        print(response.json())
    else:
        print(f"Failure with {response.status_code}: {path}")

path = "get_goals_list"
request = """{
    "filter_expression": "'no' in relationship"
}"""
run_test(path, request)

path = "get_modules_list"
request = '''{
    "goal_id_column": "goal_id_c",
    "goal_priority_column": "priority_in_goal_c",
    "goal_id": "learning",
    "filter_expression": "'female' in child_gender and 6 in age",
    "sort_columns": ["priority_in_topic"]
}'''
run_test(path, request)

path = "get_goal_name"
request = """{
    "column": "name_c",
    "language": "eng",
    "id": "safety"
}"""
run_test(path, request)

path = "get_module_name"
request = """{
    "column": "name",
    "language": "zul",
    "id": "take_a_pause"
}"""
run_test(path, request)

path = "get_numbered_goal_names"
request = """{
    "column": "name_c",
    "language": "eng",
    "ids": "safety learning develop"
}"""
run_test(path, request)

path = "get_numbered_module_names"
request = """{
    "column": "name",
    "language": "eng",
    "ids": "take_a_pause one_on_one_yc"
}"""
run_test(path, request)

path = "get_ltp_activities_list"
request = """{
    "filter_expression": "'Calm' in act_type and 17 in act_age"
}"""
run_test(path, request)
