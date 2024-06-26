import re
import sys
from datetime import datetime
from pathlib import Path
from sscsv.controllers.CsvController import CsvController
from sscsv.views.TableView import TableView
import polars as pl

class DataFrameController(object):
    def __init__(self):
        self.df = None
    
    # -- initializer --
    def load(self, path):
        """[initializer] Loads the specified CSV file."""
        self.df = CsvController(path=path).get_dataframe()
        return self

    # -- chainable --
    def select(self, columns: str) -> None:
        """[chainable] Displays the specified columns."""
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
        """[chainable] Displays rows that contain the specified values."""
        self.df = self.df.filter(pl.col(colname).is_in(values))
        return self
    
    def contains(self, colname: str, regex: str):
        """[chainable] Displays rows that contain the specified string."""
        regex = regex if type(regex) is str else str(regex)
        self.df = self.df.filter(pl.col(colname).str.contains(regex))
        return self

    def head(self, number: int = 5):
        """[chainable] Displays the first specified number of rows of the data."""
        self.df = self.df.head(number)
        return self

    def tail(self, number: int = 5):
        """[chainable] Displays the last specified number of rows of the data."""
        self.df = self.df.tail(number)
        return self
    
    def sort(self, columns: str, desc: bool = False):
        """[chainable] Sorts the data by the values of the specified column."""
        self.df = self.df.sort(columns, descending=desc)
        return self
    
    def changetz(self, colname: str, timezone_from: str = "UTC", timezone_to: str = "Asia/Tokyo", new_colname: str = None):
        """[chainable] Changes the timezone of the specified date column."""
        new_colname = new_colname if new_colname else colname
        self.df.with_columns(pl.col(colname).dt.replace_time_zone(timezone_from))
        self.df = self.df.with_columns(
            pl.col(colname).cast(pl.Datetime).dt.convert_time_zone(timezone_to).alias(new_colname)
        )
        return self
    
    # -- finalizer --
    def headers(self, plain: bool = False):
        """[finalizer] Displays the column names of the data."""
        if plain:
            print(",".join([f"\"{c}\"" for c in self.df.columns]))
        else:
            TableView.print(
                headers=["#", "Column Name"],
                values=[[str(i).zfill(2), c] for i, c in enumerate(self.df.columns)]
            )
    
    def stats(self):
        """[finalizer] Displays the statistical information of the data."""
        print(self.df.describe())       

    def showquery(self):
        """[finalizer] Displays the data processing query."""
        print(self.df)

    def show(self):
        """[finalizer] Outputs the processing results to the standard output."""
        self.df.collect().write_csv(sys.stdout)
    
    def dump(self, path: str = None):
        """[finalizer] Outputs the processing results to a CSV file."""
        def autoname():
            now = datetime.now().strftime('%Y%m%d-%H%M%S')
            query = self.df.explain(optimized=False).splitlines()[0]
            temp = re.sub(r'[^\w\s]', '-', query)
            temp = re.sub(r'-+', '-', temp)
            temp = temp.strip('-')
            temp = temp.replace(' ', '')
            temp = temp.lower()
            return f"{now}_{temp}.csv"

        path = path if path else autoname()
        self.df.collect().write_csv(path)
    
    # def __str__(self):
    #     if self.df is not None:
    #         print(self.df.collect())
    #     return ''
