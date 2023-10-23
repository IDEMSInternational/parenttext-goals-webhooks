from hooks import get_goals_list, get_modules_list, get_goal_name, get_numbered_goal_names, get_module_name, get_numbered_module_names, get_ltp_activities_list
import functions_framework
import uuid
import math
from datetime import datetime


@functions_framework.http
def serve(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # request_json = request.get_json(silent=True)
    # request_args = request.args

    request_json = request.get_json(silent=True)
    if not request_json:
        # return 'Hellooo {}!'.format(name)
        return {"error": "No Data"}, 200

    path = request.path.strip("/")
    if path == "get_goals_list":
        return get_goals_list(request_json)
    if path == "get_modules_list":
        return get_modules_list(request_json)
    if path == "get_goal_name":
        return get_goal_name(request_json)
    if path == "get_numbered_goal_names":
        return get_numbered_goal_names(request_json)
    if path == "get_module_name":
        return get_module_name(request_json)
    if path == "get_numbered_module_names":
        return get_numbered_module_names(request_json)
    if path == "get_ltp_activities_list":
        return get_ltp_activities_list(request_json)
    else:
        return {"error": "Invalid path"}, 404
