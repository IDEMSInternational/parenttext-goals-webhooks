from fastapi import FastAPI
from pydantic import BaseModel

from parenttext_goals_webhooks.hooks import Hooks


app = FastAPI()


class ListQuery(BaseModel):
    filter_expression: str = ""
    sort_columns: list[str] = list()


class ModulesListQuery(ListQuery):
    goal_id: str = ""
    goal_id_column: str = ""
    goal_priority_column: str = ""


class EntryQuery(BaseModel):
    column: str = ""
    id: str = ""


class NameQuery(EntryQuery):
    language: str = ""


class NumberedNamesQuery(NameQuery):
    ids: str = ""


@app.post("/get_goals_list")
def get_goals_list(q: ListQuery):
    return Hooks().get_goals_list(q)


@app.post("/get_modules_list")
def get_modules_list(q: ModulesListQuery):
    return Hooks().get_modules_list(q)


@app.post("/get_goal_name")
def get_goal_name(q: NameQuery):
    return Hooks().get_goal_name(q)


@app.post("/get_goal_entry")
def get_goal_entry(q: EntryQuery):
    return Hooks().get_goal_entry(q)


@app.post("/get_numbered_goal_names")
def get_numbered_goal_names(q: NumberedNamesQuery):
    return Hooks().get_numbered_goal_names(q)


@app.post("/get_module_name")
def get_module_name(q: NameQuery):
    return Hooks().get_module_name(q)


@app.post("/get_numbered_module_names")
def get_numbered_module_names(q: NumberedNamesQuery):
    return Hooks().get_numbered_module_names(q)


@app.post("/get_ltp_activities_list")
def get_ltp_activities_list(q: ListQuery):
    return Hooks().get_ltp_activities_list(q)
