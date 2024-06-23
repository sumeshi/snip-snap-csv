from sscsv.controllers.CsvController import CsvController

def select(filepath: str, columns: str) -> None:
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

    df = CsvController(path=filepath).get_dataframe()
    selected_columns = parse_columns(headers=df.columns, columns=columns)
    print(selected_columns)