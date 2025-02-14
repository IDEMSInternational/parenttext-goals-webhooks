import logging
from contextlib import asynccontextmanager
from enum import Enum
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings


from parenttext_goals_webhooks import api_version
from parenttext_goals_webhooks.hooks import Hooks
from parenttext_goals_webhooks.sheets import DataSource, JSONDataSource, temp_repo


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield
    destroy()


def init():
    global hooks
    url = settings.repo_url
    ref = settings.repo_ref

    if url and ref:
        with temp_repo(url, ref) as repo:
            logger.info(
                {
                    "msg": "Content repo cloned",
                    "url": url,
                    "ref": ref,
                    "local": str(repo),
                }
            )
            root = Path(repo) / settings.repo_path
            hooks = Hooks(db=JSONDataSource(root=root, config=settings.config_file))
            logger.info({"msg": "Content loaded", "csv_mode": False, "path": str(root)})
    else:
        cls = DataSource if settings.csv_mode else JSONDataSource
        hooks = Hooks(db=cls())
        logger.info(
            {
                "msg": "Content loaded",
                "csv_mode": settings.csv_mode,
                "path": "data",
            }
        )


def destroy():
    pass


class Settings(BaseSettings):
    repo_url: str = ""
    repo_ref: str = ""
    repo_path: str = ""
    config_file: str = "api.json"
    csv_mode: bool = False


hooks = None
settings = Settings()
app = FastAPI(
    lifespan=lifespan,
    title="ParentText Goals API",
    summary="Provides information about goals, modules and activities.",
    version=api_version(),
)


class ListQuery(BaseModel):
    filter_expression: str = ""
    sort_columns: list[str] = list()

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "filter_expression": "'no' in relationship",
                    "sort_columns": ["priority_in_topic"],
                }
            ]
        }


class ModulesListQuery(ListQuery):
    goal_id: str = ""
    goal_id_column: str = ""
    goal_priority_column: str = ""

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "filter_expression": "'female' in child_gender and 7 in age",
                    "goal_id": "relation",
                    "goal_id_column": "goal_id_c",
                    "goal_priority_column": "priority_in_goal_c",
                    "sort_columns": ["priority_in_topic"],
                }
            ]
        }


class EntryQuery(BaseModel):
    column: str = ""
    id: str = ""

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "column": "checkin_c",
                    "id": "relation",
                }
            ]
        }


class NameQuery(EntryQuery):
    language: str = ""

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "column": "name_c",
                    "language": "eng",
                    "id": "safety",
                }
            ]
        }


class NumberedNamesQuery(NameQuery):
    ids: str = ""

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "column": "name_c",
                    "language": "eng",
                    "ids": "safety",
                }
            ]
        }


class Result(BaseModel):
    text: str


class Tags(Enum):
    goals = "goals"
    modules = "modules"
    activities = "activities"
    hooks = "hooks"


@app.post(
    "/get_goals_list",
    tags=[Tags.goals],
    summary="Get goal IDs",
)
def get_goals_list(q: ListQuery) -> Result:
    """
    List goal IDs, filtered by `filter_expression` and sorted by `sort_columns`.
    """
    return Result(text=hooks.get_goals_list(q))


@app.post(
    "/get_modules_list",
    tags=[Tags.modules],
    summary="Get module IDs",
)
def get_modules_list(q: ModulesListQuery) -> Result:
    """
    Get a filtered and sorted list of module IDs given a goal ID.

    The goal ID is specified via `goal_id`. The given goal ID will be used to match
    against a particular column given in `goal_id_column`. The `goal_priority_column`
    will be used to sort topics.

    Modules will be filtered by `filter_expression`. After filtering, if more than one
    module exists for the same topic, `sort_columns` will be used to order the modules.
    """
    return Result(text=hooks.get_modules_list(q))


@app.post(
    "/get_goal_name",
    tags=[Tags.goals],
    summary="Get name of a goal",
)
def get_goal_name(q: NameQuery) -> Result:
    """
    Given an ID of a goal, and a language and column, look up the translated name in the
    respective column.
    """
    return Result(text=hooks.get_goal_name(q))


@app.post(
    "/get_goal_entry",
    tags=[Tags.goals],
    summary="Get value of a field from a goal",
)
def get_goal_entry(q: EntryQuery) -> Result:
    """
    Get the value of a particular column for a particular goal.

    The column should be a simple column (no nesting, i.e. no dots in the column name)
    of type `str`.
    """
    return Result(text=hooks.get_goal_entry(q))


@app.post(
    "/get_numbered_goal_names",
    tags=[Tags.goals],
    summary="Get numbered list of goal names",
)
def get_numbered_goal_names(q: NumberedNamesQuery) -> Result:
    """
    Given a space separated list of goal IDs, a language, and column, look up the
    translated name in the respective column, and produce a numbered list of names.
    """
    return Result(text=hooks.get_numbered_goal_names(q))


@app.post(
    "/get_module_name",
    tags=[Tags.modules],
    summary="Get name of a module",
)
def get_module_name(q: NameQuery) -> Result:
    """
    Given an ID of a module, and a language and column, look up the translated name in
    the respective column.
    """
    return Result(text=hooks.get_module_name(q))


@app.post(
    "/get_numbered_module_names",
    tags=[Tags.modules],
    summary="Get numbered list of module names",
)
def get_numbered_module_names(q: NumberedNamesQuery) -> Result:
    """
    Given a space separated list of module IDs, a language, and column, look up the
    translated name in the respective column, and produce a numbered list of names.
    """
    return Result(text=hooks.get_numbered_module_names(q))


@app.post(
    "/get_ltp_activities_list",
    tags=[Tags.activities],
    summary="Get LTP activity IDs",
)
def get_ltp_activities_list(q: ListQuery) -> Result:
    """
    Get list of LTP activity IDs, filtered by `filter_expression` and sorted by
    `sort_columns`.
    """
    return Result(text=hooks.get_ltp_activities_list(q))
