from rpft.parsers.common.sheetparser import SheetParser
from rpft.parsers.common.cellparser import CellParser
from rpft.parsers.common.rowparser import RowParser, ParserModel
from rpft.parsers.sheets.csv_sheet_reader import CSVSheetReader
from rpft.parsers.sheets.xlsx_sheet_reader import XLSXSheetReader

from models import GoalDataGlobal, GoalModuleLinkGlobal, ModuleDataGlobal, LTPActivities

def get_sheet(name, model, testing=False):
    path = f"data/{name}.csv"
    if testing:
        path = f"test_data/{name}.csv"
    reader = CSVSheetReader(path)
    content = reader.get_main_sheet()
    rowparser = RowParser(model, CellParser())
    sheetparser = SheetParser(rowparser, content)
    rows = sheetparser.parse_all()
    return {row.ID: row for row in rows}

def get_module_data_global_sheet(testing=False):
    return get_sheet("module_data_global", ModuleDataGlobal, testing)

def get_goal_module_link_global_sheet(testing=False):
    return get_sheet("goal_module_link_global", GoalModuleLinkGlobal, testing)

def get_goal_data_global_sheet(testing=False):
    return get_sheet("goal_data_global", GoalDataGlobal, testing)

def get_ltp_activities_sheet(testing=False):
    return get_sheet("ltp_activities", LTPActivities, testing)
