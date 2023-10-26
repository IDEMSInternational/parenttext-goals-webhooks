'''
This is a simple script for manually testing that the webhook
actually works.

The actual functionality of the webhooks is covered by the
automated tests.
'''

import argparse
import requests
import json

class WebhookTester:

    def __init__(self, url):
        self.successes = 0
        self.total = 0
        self.base_url = url

    def run_test(self, path, request):
        url = self.base_url + '/' + path
        data = json.loads(request)
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Success: {path}")
            print(response.json())
            self.successes += 1
        elif response.status_code == 404:
            print(f"Failure with {response.status_code}: {path}")
            print(response.json())
        else:
            print(f"Failure with {response.status_code}: {path}")
        self.total += 1

    def print_summary(self):
        print(f"{self.successes} out of {self.total} successful")


def run_tests(url):
    wt = WebhookTester(url)

    path = "get_goals_list"
    request = """{
        "filter_expression": "'no' in relationship"
    }"""
    wt.run_test(path, request)

    path = "get_modules_list"
    request = '''{
        "goal_id_column": "goal_id_c",
        "goal_priority_column": "priority_in_goal_c",
        "goal_id": "learning",
        "filter_expression": "'female' in child_gender and 6 in age",
        "sort_columns": ["priority_in_topic"]
    }'''
    wt.run_test(path, request)

    path = "get_goal_name"
    request = """{
        "column": "name_c",
        "language": "eng",
        "id": "safety"
    }"""
    wt.run_test(path, request)

    path = "get_module_name"
    request = """{
        "column": "name",
        "language": "zul",
        "id": "take_a_pause"
    }"""
    wt.run_test(path, request)

    path = "get_numbered_goal_names"
    request = """{
        "column": "name_c",
        "language": "eng",
        "ids": "safety learning develop"
    }"""
    wt.run_test(path, request)

    path = "get_numbered_module_names"
    request = """{
        "column": "name",
        "language": "eng",
        "ids": "take_a_pause one_on_one_yc"
    }"""
    wt.run_test(path, request)

    path = "get_ltp_activities_list"
    request = """{
        "filter_expression": "'Calm' in act_type and 17 in act_age"
    }"""
    wt.run_test(path, request)

    wt.print_summary()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Send requests to deployed app to ensure they work"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "url",
        help="The base URL of the service to test",
    )

    args = parser.parse_args()
    run_tests(args.url)


if __name__ == "__main__":
    main()
