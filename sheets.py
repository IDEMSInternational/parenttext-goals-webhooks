from rpft.parsers.common.sheetparser import SheetParser
from rpft.parsers.common.cellparser import CellParser
from rpft.parsers.common.rowparser import RowParser, ParserModel
from rpft.parsers.sheets import CSVSheetReader, XLSXSheetReader

from models import GoalDataGlobal, GoalModuleLinkGlobal, ModuleDataGlobal, LTPActivities

def get_sheet(name, model, testing=False):
    reader = CSVSheetReader("test_data" if testing else "data")
    content = reader.get_sheet(name)
    rowparser = RowParser(model, CellParser())
    sheetparser = SheetParser(rowparser, content.table)
    rows = sheetparser.parse_all()
    return {row.ID: row for row in rows}

def get_module_data_global_sheet(testing=False):
    return get_sheet("module_data_global", ModuleDataGlobal, testing)

def get_goal_module_link_global_sheet(testing=False):
    return get_sheet("goal_topic_link_global", GoalModuleLinkGlobal, testing)

def get_goal_data_global_sheet(testing=False):
    return get_sheet("goal_data_global", GoalDataGlobal, testing)

def get_ltp_activities_sheet(testing=False):
    return get_sheet("ltp_activities", LTPActivities, testing)
