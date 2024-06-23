from sscsv.controllers.CsvController import CsvController
from sscsv.views.TableView import TableView

def headers(filepath: str, plain: bool = False) -> None:
    df = CsvController(path=filepath).get_dataframe()
    if plain:
        print(",".join([f"\"{c}\"" for c in df.columns]))
    else:
        TableView.print(
            headers=["#", "Column Name"],
            values=[[str(i).zfill(2), c] for i, c in enumerate(df.columns)]
        )