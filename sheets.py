from rpft.parsers.common.sheetparser import SheetParser
from rpft.parsers.common.cellparser import CellParser
from rpft.parsers.common.rowparser import RowParser, ParserModel
from rpft.parsers.sheets.csv_sheet_reader import CSVSheetReader
from rpft.parsers.sheets.xlsx_sheet_reader import XLSXSheetReader

from models import GoalDataGlobal, GoalModuleLinkGlobal, ModuleDataGlobal

def get_sheet(name, model):
    reader = CSVSheetReader(f"data/{name}.csv")
    content = reader.get_main_sheet()
    rowparser = RowParser(model, CellParser())
    sheetparser = SheetParser(rowparser, content)
    rows = sheetparser.parse_all()
    return {row.ID: row for row in rows}

def get_module_data_global_sheet():
    return get_sheet("module_data_global", ModuleDataGlobal)

def get_goal_module_link_global_sheet():
    return get_sheet("goal_module_link_global", GoalModuleLinkGlobal)

def get_goal_data_global_sheet():
    return get_sheet("goal_data_global", GoalDataGlobal)



# def get_sheet(name):
#     outdata = {}
#     with open(f"data/{name}.csv", newline="") as csvfile:
#         reader = csv.DictReader(csvfile)
#         headers = reader.fieldnames
#         for row in reader:
#             outdata[row["ID"]] = row
#         return headers, outdata
