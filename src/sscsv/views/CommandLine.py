import fire
from sscsv.controllers.CsvFile import load_csv

def headers(filename: str, plain=False) -> None:
    df = load_csv(filename)
    if plain:
        print(",".join([f"\"{c}\"" for c in df.columns]))
    else:
        print("\n".join([f"{str(i).zfill(2)}: {c}" for i, c in enumerate(df.columns)]))

def entry_point():
    fire.Fire({"headers": headers})