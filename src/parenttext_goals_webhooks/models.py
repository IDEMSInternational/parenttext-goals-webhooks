from rpft.parsers.creation.datarowmodel import DataRowModel
from rpft.parsers.common.rowparser import ParserModel

from typing import List



class GoalDataGlobal(DataRowModel):
    priority_c: str = ""
    priority2_c: str = ""
    priority_p: str = ""
    priority_t: str = ""
    priority2_t: str = ""
    relationship: List[str] = []
    checkin_c: str = ""
    checkin_p: str = ""
    checkin_t: str = ""
    name_c: dict = {}
    name_t: dict = {}
    parent_gender: str = ""


class GoalModuleLinkGlobal(DataRowModel):
    goal_id_c: str = ""
    priority_in_goal_c: str = ""
    goal_id_p: str = ""
    priority_in_goal_p: str = ""
    goal_id_t: str = ""
    priority_in_goal_t: str = ""


class ModuleDataGlobal(DataRowModel):
    topic_ID: str = ""
    priority_in_topic: str = ""
    age: List[int] = []
    child_gender: List[str] = []
    name: dict = {}
    name_c: dict = {}


class LTPActivities(DataRowModel):
    name: str = ""
    text: str = ""
    act_type: List[str] = []
    act_age: List[int] = []
    use_in_demo: str = ""
    attached_single_doc: str = ""
