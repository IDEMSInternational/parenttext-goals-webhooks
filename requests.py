import csv
import copy


def get_sheet(name):
    outdata = {}
    with open(f"data/{name}.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        for row in reader:
            outdata[row["ID"]] = row
        return headers, outdata


def get_modules_list(request_json):
    general_topicids = get_general_topicids(request_json)
    explicit_topicids = get_explicit_topicids(request_json, general_topicids)
    text = " ".join(explicit_topicids)
    return {"text": text}, 200


def get_explicit_topicids(request_json, topicsid_list):
    headers, module_data = get_sheet("module_data_global")
    all_topics = []
    for topic_id in topicsid_list:
        new_subtopics = []
        topics = [m for m in module_data.values() if m["topic_ID"] == topic_id]
        new_subtopics = filter_and_sort(request_json, topics)
        all_topics += new_subtopics
    return get_ids_list(all_topics)


def get_general_topicids(request_json):
    # Get the list of topic IDs associated with the specified goal.
    headers, goal_data = get_sheet("goal_module_link_global")
    goal_id_column = request_json["goal_id_column"]
    goal_priority_column = request_json["goal_priority_column"]
    goal_id = request_json["goal_id"]
    topics_list = []
    for _, row in goal_data.items():
        if row[goal_id_column] == goal_id:
            topics_list.append(row)
    topics_list = sort_rows([goal_priority_column], topics_list)
    return get_ids_list(topics_list)


def get_ids_list(rows):
    return list(map(lambda x: x["ID"], rows))


def get_ids_string(rows):
    ids = get_ids_list(rows)
    return " ".join(ids)


def filter_rows(filter_expression, rows):
    new_row_data = []
    for row in rows:
        if eval(filter_expression, {}, row) == True:
            new_row_data.append(row)
    return new_row_data


def sort_rows(sort_columns, rows):
    output = copy.deepcopy(rows)
    if len(rows) <= 1:
        # Don't filter out empty sort column if there is only 1 row
        return rows
    # Because sort is stable, we sort backwards
    for column in sort_columns[::-1]:
        # remove empty entries
        output = list(filter(lambda x: x[column], output))
        # sort
        output.sort(key=lambda x: x[column])
    return output


def filter_and_sort(request_json, rows):
    if "filter_expression" in request_json:
        filter_expression = request_json["filter_expression"]
        rows = filter_rows(filter_expression, rows)
    if "sort_columns" in request_json:
        sort_columns = request_json["sort_columns"]
        rows = sort_rows(sort_columns, rows)
    return rows


def get_goals_list(request_json):
    headers, goal_data = get_sheet("goal_data_global")
    output = goal_data.values()
    output = filter_and_sort(request_json, output)
    text = get_ids_string(output)
    return {"text": text}, 200


def get_goal_name(request_json):
    headers, goal_data = get_sheet("goal_data_global")
    return get_name(request_json, goal_data)


def get_module_name(request_json):
    headers, module_data = get_sheet("module_data_global")
    return get_name(request_json, module_data)


def get_name(request_json, data):
    column_base = request_json["column"]
    language = request_json["language"]
    goal_id = request_json["goal_id"]
    row = data[goal_id]
    string = row[f"{column_base}.{language}"]
    return {"text": string}, 200
