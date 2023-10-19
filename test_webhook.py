'''
This is a simple script for manually testing that the webhook
actually works.

The actual functionality of the webhooks is covered by the
automated tests.
'''

import requests
import json

baseurl = "https://europe-west2-glossy-attic-237012.cloudfunctions.net/parenttext-individualize-module-list"
path = "get_modules_list"
url = baseurl + '/' + path
request = '''{
    "goal_id_column": "goal_id_c",
    "goal_priority_column": "priority_in_goal_c",
    "goal_id": "learning",
    "filter_expression": "'female' in child_gender and 6 in age",
    "sort_columns": ["priority_in_topic"]
}'''
data = json.loads(request)

response = requests.post(url, json=data)

print(response.json())


