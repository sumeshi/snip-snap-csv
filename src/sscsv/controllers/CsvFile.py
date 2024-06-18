import polars as pl

def load_csv(filename: str) -> pl.DataFrame:
    df = pl.read_csv(
        filename,
        rechunk=True,
        truncate_ragged_lines=True,
    )

    return df