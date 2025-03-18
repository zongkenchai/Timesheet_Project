import polars as pl
import polars.selectors as cs
import pendulum
import pandas as pd
import os

# File name
file_name = "Timesheet.xlsx"

# List of months to process
months = ["January", "February", "March", "April", "May"]

# Process each sheet dynamically
timesheet_data = []
for i, month in enumerate(months, start=1):
    sheet_data = (
        pl.read_excel(file_name, sheet_name=month)
        .melt(
            id_vars=["JOB CODE"],
            value_vars=cs.numeric(),
            variable_name="employee_code",
            value_name="duration",
        )
        .select(
            "employee_code",
            pl.col("JOB CODE").alias("project_code"),
            pl.lit(pendulum.date(2024, i, 1)).alias("month"),
            pl.col("duration").cast(pl.Float64),
        )
    )
    timesheet_data.append(sheet_data)

# Combine all months into a single DataFrame
timesheet_df = pl.concat(timesheet_data).filter(pl.col("duration") > 0)

# Convert to Pandas for Excel writing
pandas_timesheet_df = timesheet_df.to_pandas()

# Write to Excel (append if file exists)
with pd.ExcelWriter(
    file_name,
    engine="openpyxl",
    mode="a" if os.path.exists(file_name) else "w",
    if_sheet_exists="replace",
) as writer:
    pandas_timesheet_df.to_excel(writer, sheet_name="Combined", index=False)

# Print the final dataframe
print(timesheet_df)
