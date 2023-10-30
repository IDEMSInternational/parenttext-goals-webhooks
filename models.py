from rpft.parsers.creation.datarowmodel import DataRowModel
from rpft.parsers.common.rowparser import ParserModel

from typing import List

class Language(ParserModel):
    eng: str = ""
    zul: str = ""
    hau: str = ""
    msa: str = ""

class GoalDataGlobal(DataRowModel):
    priority_c: str = ""
    priority_p: str = ""
    priority_t: str = ""
    relationship: List[str] = []
    name_c: Language = Language()
    name_t: Language = Language()

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
    name: Language = Language()
    name_c: Language = Language()

class LTPActivities(DataRowModel):
    name: str = ""
    text: str = ""
    act_type: List[str] = []
    act_age: List[int] = []
    use_in_demo: str = ""
