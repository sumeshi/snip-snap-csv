# snip-snap-csv
A tool designed for rapid data processing and filtering.

## Archtecture
```
initialize method -> chainable methods... -> finalize mthod
```

### initialize methods
- load

### chainable methods
- select
- isin
- contains
- head
- tail
- sort
- changetz

### finalize methods
- headers
- stat
- showquery
- show
- dump

## Planned Features:
- CSV cache (.pkl)
- Extraction of specific columns
- Filtering based on specific conditions (OR, AND conditions)
- Sorting
- Cell text conversion
- Grouping for operations like count
- Joining with other tables
- Export Config
