"""
pmedpc: A tool to extract data from MedPC files and write to csv.

By: Beverly Peng
"""

_epilog = """

Example

Open specified MedPC file, extract relevant data and write
to file <filename>_format.csv

python -m pmedpc <filename>
"""

import sys
from . import utils
from . import extract_medpc
import numpy as np
from datetime import datetime

def main():
  # Reading in arguments
  args = utils._parse_args(sys.argv[1:],
                          epilog=_epilog,
                          description=__doc__)
  args_1 = sys.argv[1] # filename

  ### Extracting data from MedPC files ###
  data = extract_medpc.MedPC([args_1])
  data.medpc_to_df()
  df = data.getRaw().astype(str)

  ### Minor edits to dataframe ###
  # Adding cohort from filename
  # df["cohort"] = ["C" + val.split("Cohort ")[1].split("/")[0] for val in df["file"]]
  # Capitalizing subject
  df["subject"] = [val.upper() for val in df["subject"]]
  # Inserting filename
  df["file"] = [val.split("/")[-1] for val in df["file"]]
  # Comment out if not including data where subject is missing
  # df = df[~df["subject"].isin(["", "0"])]
  # df.index = range(df.shape[0])
  # Fixing dates
  values = []
  for val in df["start_date"]: 
      val = val.replace("/", "-")
      val = "20" + "-".join([val.split("-")[2], val.split("-")[0], val.split("-")[1]])
      values.append(val)
  df["start_date"] = values
  values = []
  for val in df["end_date"]: 
      val = val.replace("/", "-")
      val = "20" + "-".join([val.split("-")[2], val.split("-")[0], val.split("-")[1]])
      values.append(val)
  df["end_date"] = values
  # Making experiment easier to read
  df["experiment"] = [val.lower().replace(" ", "_").replace("-", "_").replace("__", "_") for val in df["experiment"]]
  # Making msn easier to read
  df["msn"] = [val.lower().replace(" ", "_").replace("-", "_").replace("__", "_") for val in df["msn"]]
  values = []
  for val in df["experiment"]: 
      if "30" in val and ("2" in val or "both" in val): 
          values.append("30min_2levers")
      elif "2" in val and "20" in val: 
          values.append("20min_2levers")
      else: 
  #         values.append("")
          values.append(val.replace(" ", "_"))
  df["experiment"] = values

  # Getting saving first value as separate column
  # a, l, r, w
  for col in ["a", "l", "r", "w"]: 
    if col not in list(df.columns): 
        continue
    for i in range(31): 
        values = []
        for val in df[col]: 
            val = val.split(",")
            if len(val) != 31: 
                # Add error statement
                break
            val = val[0].replace("[", "")
            print(val)
            values.append(val)
        # df[col + "_" + str(i)] = values
        if i == 0: 
            df[f"{col}_total"] = values
        else: 
            df[f"{col}_{i}"] = values


  print()

  # Printing File Summary
  print("FILE SUMMARY")
  print("columns found:", list(df.columns))
  for col in df.columns: 
    if len(col) < 2: continue
    print(col, ":", list(np.unique(df[col])))
  
  # filename = args_1 + "_" + extract_medpc.get_timestamp() + ".csv"
  filename = f"{args_1}_{extract_medpc.get_timestamp()}.csv"
  print("saved to", filename)
  df.to_csv(filename, index = False)

main()
