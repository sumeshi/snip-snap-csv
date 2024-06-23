from sscsv.controllers.CsvController import CsvController
from polars import DataFrame

def tail(filepath: str, number: int = 5) -> DataFrame:
    df = CsvController(path=filepath).get_dataframe()
    return df.tail(number)