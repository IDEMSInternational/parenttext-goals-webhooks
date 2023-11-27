import copy

from sheets import DataSource


def map_ids(rows):
    return list(map(lambda x: x.ID, rows))


def filter_rows(filter_expression, rows):
    new_row_data = []
    for row in rows:
        if eval(filter_expression, {}, dict(row)) is True:
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
        output = list(filter(lambda x: getattr(x, column), output))
        # sort
        output.sort(key=lambda x: getattr(x, column))
    return output


def filter_and_sort(request_json, rows):
    if "filter_expression" in request_json:
        filter_expression = request_json["filter_expression"]
        rows = filter_rows(filter_expression, rows)
    if "sort_columns" in request_json:
        sort_columns = request_json["sort_columns"]
        rows = sort_rows(sort_columns, rows)
    return rows


def get_ids_list(request_json, data):
    output = data.values()
    output = filter_and_sort(request_json, output)
    goals = map_ids(output)
    text = " ".join(goals)
    return {"text": text}, 200


class Hooks:
    def __init__(self, data_dir="data"):
        self.db = DataSource(source=data_dir)

    def get_modules_list(self, request_json):
        general_topicids = self.get_general_topicids(request_json)
        explicit_topicids = self.get_explicit_topicids(request_json, general_topicids)
        text = " ".join(explicit_topicids)

        return {"text": text}, 200

    def get_explicit_topicids(self, request_json, topicsid_list):
        all_topics = []

        for topic_id in topicsid_list:
            new_subtopics = []
            topics = [m for m in self.db.modules().values() if m.topic_ID == topic_id]
            new_subtopics = filter_and_sort(request_json, topics)
            all_topics += new_subtopics

        return map_ids(all_topics)

    def get_general_topicids(self, request_json):
        # Get the list of topic IDs associated with the specified goal.
        goal_id_column = request_json["goal_id_column"]
        goal_priority_column = request_json["goal_priority_column"]
        goal_id = request_json["goal_id"]
        topics_list = []
        for _, row in self.db.goal_topic_links().items():
            if getattr(row, goal_id_column) == goal_id:
                topics_list.append(row)
        topics_list = sort_rows([goal_priority_column], topics_list)
        return map_ids(topics_list)

    def get_goals_list(self, request_json):
        return get_ids_list(request_json, self.db.goals())

    def get_ltp_activities_list(self, request_json):
        return get_ids_list(request_json, self.db.ltp_activities())

    def get_goals_names_list_txt(self, request_json):
        goals = self.get_goals_list(request_json)
        text = " ".join(goals)
        return {"text": text}, 200

    def get_goal_name(self, request_json):
        text = self.get_name(request_json, self.db.goals())
        return {"text": text}, 200

    def get_numbered_names(self, request_json, data):
        ids = request_json["ids"].split()
        names = [self.get_name(request_json, data, goal_id) for goal_id in ids]
        numbered_names = [f"{i+1}. {name}" for i, name in enumerate(names)]
        numbered = "\n".join(numbered_names)
        return numbered

    def get_numbered_module_names(self, request_json):
        text = self.get_numbered_names(request_json, self.db.modules())
        return {"text": text}, 200

    def get_numbered_goal_names(self, request_json):
        text = self.get_numbered_names(request_json, self.db.goals())
        return {"text": text}, 200

    def get_module_name(self, request_json):
        text = self.get_name(request_json, self.db.modules())
        return {"text": text}, 200

    def get_name(self, request_json, data, goal_id=None):
        column_base = request_json["column"]
        language = request_json["language"]
        goal_id = goal_id or request_json["id"]
        row = data[goal_id]
        string = getattr(getattr(row, column_base), language)
        return string
