from rpft.parsers.common.sheetparser import SheetParser
from rpft.parsers.common.cellparser import CellParser
from rpft.parsers.common.rowparser import RowParser
from rpft.parsers.sheets import CSVSheetReader

from models import GoalDataGlobal, GoalModuleLinkGlobal, ModuleDataGlobal, LTPActivities


class DataSource:
    def __init__(self, source="data"):
        self.source = source

    def get_sheet(self, name, model):
        reader = CSVSheetReader(self.source)

        try:
            table = reader.get_sheet(name).table
        except AttributeError:
            return {}

        parser = SheetParser(
            RowParser(model, CellParser()),
            table,
        )
        return {row.ID: row for row in parser.parse_all()}

    def modules(self):
        return self.get_sheet("module_data", ModuleDataGlobal)

    def goal_topic_links(self):
        return self.get_sheet("goal_topic_link", GoalModuleLinkGlobal)

    def goals(self):
        return self.get_sheet("goal_data", GoalDataGlobal)

    def ltp_activities(self):
        return self.get_sheet("ltp_activities", LTPActivities)
