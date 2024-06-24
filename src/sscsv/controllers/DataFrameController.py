import sys
from pathlib import Path
from sscsv.controllers.CsvController import CsvController
from sscsv.views.TableView import TableView
import polars as pl

class DataFrameController(object):
    def __init__(self):
        self.df = None
    
    # initialize methods
    def load(self, path):
        self.df = CsvController(path=path).get_dataframe()
        return self

    # chainable methods
    def headers(self, plain: bool = False) -> None:
        if plain:
            print(",".join([f"\"{c}\"" for c in self.df.columns]))
        else:
            TableView.print(
                headers=["#", "Column Name"],
                values=[[str(i).zfill(2), c] for i, c in enumerate(self.df.columns)]
            )

    def select(self, columns: str) -> None:
        def parse_columns(headers: list[str], columns: tuple[str]):
            if type(columns) is tuple:
                columns = ",".join(columns)
            parsed_columns = list()
            for term in columns.split(','):
                if '-' not in term:
                    parsed_columns.append(term)
                else:
                    flag_extract = False
                    start, end = term.split('-')
                    for h in headers:
                        if h == start:
                            flag_extract = True
                        if flag_extract:
                            parsed_columns.append(h)
                        if h == end:
                            flag_extract = False
            return parsed_columns
        selected_columns = parse_columns(headers=self.df.columns, columns=columns)
        self.df = self.df.select(selected_columns)
        return self
    
    def search(self, query: str):

        return self

    def head(self, number: int = 5):
        self.df = self.df.head(number)
        return self

    def tail(self, number: int = 5):
        self.df = self.df.tail(number)
        return self
    
    def sort(self, columns: str, desc: bool = False):
        self.df = self.df.sort(columns, descending=desc)
        return self
    
    # finalize methods
    def show(self):
        self.df.collect().write_csv(sys.stdout)
    
    def dump(self, path: str):
        self.df.collect().write_csv(path)
    
    def __str__(self):
        print(self.df.collect())
        return ''
