import functions_framework
from hooks import Hooks


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

    h = Hooks()

    path = request.path.strip("/")
    if path == "get_goals_list":
        return h.get_goals_list(request_json)
    if path == "get_modules_list":
        return h.get_modules_list(request_json)
    if path == "get_goal_name":
        return h.get_goal_name(request_json)
    if path == "get_numbered_goal_names":
        return h.get_numbered_goal_names(request_json)
    if path == "get_module_name":
        return h.get_module_name(request_json)
    if path == "get_numbered_module_names":
        return h.get_numbered_module_names(request_json)
    if path == "get_ltp_activities_list":
        return h.get_ltp_activities_list(request_json)
    else:
        return {"error": "Invalid path"}, 404
