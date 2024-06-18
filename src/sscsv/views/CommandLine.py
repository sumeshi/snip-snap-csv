import fire
from sscsv.controllers.CsvFile import load_csv

def headers(filename: str, plain=False) -> None:
    df = load_csv(filename)
    if plain:
        print(",".join([f"\"{c}\"" for c in df.columns]))
    else:
        print("\n".join([f"{str(i).zfill(2)}: {c}" for i, c in enumerate(df.columns)]))


def select(filename: str, columns: str) -> None:
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

    df = load_csv(filename)
    selected_columns = parse_columns(headers=df.columns, columns=columns)
    print(selected_columns)


def entry_point():
    fire.Fire({
        "headers": headers,
        "select": select,
    })
