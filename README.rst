::
  Usage: decol [OPTIONS] INPUT OUTPUT
  
  A tool to delete columns from a CSV file.

  Options:
    -c, --columns COLUMNS  Comma-separated list of 1-based column indexes to
                           remove. Negative integers will index from the end.
                           Mutually exclusive with --headers.
    -H, --headers HEADERS  Comma-separated list of columns to remove by first-
                           line header. Mutually exclusive with --columns.
    -s, --sep SEPARATOR    Column separator.  [default: ,]
    --keep TEXT            Keep only the specified columns in the order
                           specified in --columns or --headers.  [default:
                           False]
    --version              Show the version and exit.
    -h, --help             Show this message and exit.
