import datamancer

proc processCsv*(csvFile: string = "Security.csv") =
  let df: DataFrame = readCSV(csvFile)
  echo df

  echo "First 5 rows of the DataFrame:"
  echo df.head(5)
