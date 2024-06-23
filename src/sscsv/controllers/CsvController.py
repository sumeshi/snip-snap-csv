from pathlib import Path
import polars as pl

class CsvController(object):
    def __init__(self, path):
        self.path: Path = path

    def get_dataframe(self) -> pl.DataFrame:
        df = pl.read_csv(
            self.path,
            rechunk=True,
            truncate_ragged_lines=True,
        )
        return df
