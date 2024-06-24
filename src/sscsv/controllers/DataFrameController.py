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
    
    def isin(self, colname: str, values: list):
        self.df = self.df.filter(pl.col(colname).is_in(values))
        return self
    
    def contains(self, colname: str, regex: str):
        self.df = self.df.filter(pl.col(colname).str.contains(regex))
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
    
    def changetz(self, colname: str, timezone_from: str = "UTC", timezone_to: str = "Asia/Tokyo", new_colname: str = None):
        new_colname = new_colname if new_colname else colname
        self.df.with_columns(pl.col(colname).dt.replace_time_zone(timezone_from))
        self.df = self.df.with_columns(
            pl.col(colname).cast(pl.Datetime).dt.convert_time_zone(timezone_to).alias(new_colname)
        )
        return self
    
    # finalize methods
    def headers(self, plain: bool = False):
        if plain:
            print(",".join([f"\"{c}\"" for c in self.df.columns]))
        else:
            TableView.print(
                headers=["#", "Column Name"],
                values=[[str(i).zfill(2), c] for i, c in enumerate(self.df.columns)]
            )
    
    def stat(self):
        print(self.df.describe())       

    def showquery(self):
        print(self.df)

    def show(self):
        self.df.collect().write_csv(sys.stdout)
    
    def dump(self, path: str):
        self.df.collect().write_csv(path)
    
    def __str__(self):
        print(self.df.collect())
        return ''
