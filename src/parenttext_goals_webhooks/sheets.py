import json
from dataclasses import dataclass
from pathlib import Path

from rpft.parsers.common.cellparser import CellParser
from rpft.parsers.common.rowparser import RowParser
from rpft.parsers.common.sheetparser import SheetParser
from rpft.parsers.sheets import CSVSheetReader, JSONSheetReader

from parenttext_goals_webhooks.models import (
    GoalDataGlobal,
    GoalModuleLinkGlobal,
    LTPActivities,
    ModuleDataGlobal,
)


class DataSource:
    def __init__(self, source="data"):
        self.reader = CSVSheetReader(source)

    def get_sheet(self, name, model):
        try:
            table = self.reader.get_sheet(name).table
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


@dataclass
class Source:
    book: str
    model: str
    resource: str
    sheet: str


class JSONDataSource:

    def __init__(self, root="data", config="api.json"):
        self.resources = {}

        with open(Path(root) / config, "r") as f:
            sheets = json.load(f).get("sheets")

        sources = [Source(**source) for source in sheets.get("goals_api_sources")]
        readers = {
            book: JSONSheetReader(Path(root) / book)
            for book in {source.book for source in sources}
        }

        for source in sources:
            table = readers[source.book].get_sheet(source.sheet).table
            rows = {
                o.ID: o
                for o in SheetParser(
                    RowParser(globals()[source.model], CellParser()),
                    table,
                ).parse_all()
            }

            if source.resource in self.resources:
                self.resources[source.resource].update(rows)
            else:
                self.resources[source.resource] = rows

    def _get(self, name):
        return self.resources.get(name, [])

    def goals(self):
        return self._get("goals")

    def goal_topic_links(self):
        return self._get("goal_topic_links")

    def modules(self):
        return self._get("modules")

    def ltp_activities(self):
        return self._get("ltp_activities")


class Repo:

    def __init__(self):
        pass
