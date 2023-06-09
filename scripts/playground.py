# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# !mdb-export Data.mdb Info > Info.csv
# !mdb-export Data.mdb FILE > FILE.csv
import pandas as pd

# Load FILE.csv and Info.csv into pandas dataframes
file_df = pd.read_csv("FILE.csv")
info_df = pd.read_csv("Info.csv")

# Merge the two dataframes on the 'pid' column
merged_df = pd.merge(file_df, info_df, on="pid", suffixes=("_file", "_info"))

# Filter out rows where Next_Date is NaN
merged_df = merged_df[merged_df["Next_Date"].notna()]

# Group the merged dataframe by OSN_NO and get the last (i.e. most recent) Next_Date for each group
grouped_df = merged_df.groupby("OSN_NO_file")["Next_Date"].last().reset_index()

# Merge the grouped dataframe with the original merged dataframe to get the Party_Name column
final_df = pd.merge(
    grouped_df, merged_df[["OSN_NO_file", "Party_Name", "Work_Done_file"]], on="OSN_NO_file"
).drop_duplicates()

# Rename the 'OSN_NO_file' column to 'OSN_NO'
final_df = final_df.rename(columns={"OSN_NO_file": "OSN_NO", "Work_Done_file": "Work_Done"})

final_df["Party_Name"] = final_df["Party_Name"].str.replace("1", "'")

# Save the final dataframe to data.csv
final_df.to_csv("data.csv", index=False, columns=["OSN_NO", "Party_Name", "Next_Date", "Work_Done"])

indexed_final_df = pd.read_csv("data.csv")
indexed_final_df = indexed_final_df.reset_index()
indexed_final_df.to_csv("data.csv", index=False)
# -

final_df