# snip-snap-csv
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

A tool designed for rapid data processing and filtering, specifically tailored for handling CSV files for log analysis.

> [!NOTE]  
> This project is in the early stages of development. Please be aware that frequent changes and updates are likely to occur.


## Usage
```bash
$ sscsv {{initializer}} {{Arguments}} - {{chainable}} {{Arguments}} - {{chainable}} {{Arguments}} - {{finalizer}} {{Arguments}}
```

e.g.
Below is an example of reading a CSV file, extracting rows that contain 4624 in the EventID column, and displaying the top 3 rows them sorted by the Timestamp column.
```bash
$ sscsv load Security.csv - isin 'Event ID' 4624 - sort 'Date and Time' - head 3
2024-06-26T17:29:19+0000 [DEBUG] 1 files are loaded. Security.csv
2024-06-26T17:29:19+0000 [DEBUG] filter condition: 4624 in Event ID
2024-06-26T17:29:19+0000 [DEBUG] sort by Date and Time (asc).
2024-06-26T17:29:19+0000 [DEBUG] heading 3 lines.
shape: (3, 5)
┌─────────────┬───────────────────────┬─────────────────────────────────┬──────────┬───────────────┐
│ Level       ┆ Date and Time         ┆ Source                          ┆ Event ID ┆ Task Category │
│ ---         ┆ ---                   ┆ ---                             ┆ ---      ┆ ---           │
│ str         ┆ str                   ┆ str                             ┆ i64      ┆ str           │
╞═════════════╪═══════════════════════╪═════════════════════════════════╪══════════╪═══════════════╡
│ Information ┆ 10/6/2016 01:00:55 PM ┆ Microsoft-Windows-Security-Aud… ┆ 4624     ┆ Logon         │
│ Information ┆ 10/6/2016 01:04:05 PM ┆ Microsoft-Windows-Security-Aud… ┆ 4624     ┆ Logon         │
│ Information ┆ 10/6/2016 01:04:10 PM ┆ Microsoft-Windows-Security-Aud… ┆ 4624     ┆ Logon         │
└─────────────┴───────────────────────┴─────────────────────────────────┴──────────┴───────────────┘
```


## Archtecture
```
initializer -> chainable manipulations... -> finalizer
```

### initializer
- load

### chainable manipulation
- select
- isin
- contains
- head
- tail
- sort
- changetz

### finalizer
- headers
- stat
- showquery
- show
- dump

## Planned Features:
- CSV cache (.pkl)
- Filtering based on specific conditions (OR, AND conditions)
- Grouping for operations like count
- Joining with other tables
- Config Batch
- Export Config

## License
snip-snap-csv is released under the [MIT](https://github.com/sumeshi/snip-snap-csv/blob/master/LICENSE) License.
