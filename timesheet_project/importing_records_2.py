import polars as pl
import polars.selectors as cs
import pendulum
import pandas as pd
import os 
file_name = 'Timesheet.xlsx'


timesheet_january = pl.read_excel(file_name, sheet_name='January')\
    .melt(
        id_vars=['JOB CODE'],
        value_vars=cs.numeric(),
        variable_name='employee_code',
        value_name='duration'
    )\
    .select(
        'employee_code',
        pl.col('JOB CODE').alias('project_code'),
        pl.lit(pendulum.parse('2024-01-01').date()).alias('month'),
        pl.col('duration').cast(pl.Float64)
    )
    
timesheet_february = pl.read_excel(file_name, sheet_name='February')\
    .melt(
        id_vars=['JOB CODE'],
        value_vars=cs.numeric(),
        variable_name='employee_code',
        value_name='duration'
    )\
    .select(
        'employee_code',
        pl.col('JOB CODE').alias('project_code'),
        pl.lit(pendulum.parse('2024-02-01').date()).alias('month'),
        pl.col('duration').cast(pl.Float64)
    )
    
    
timesheet_march = pl.read_excel(file_name, sheet_name='March')\
    .melt(
        id_vars=['JOB CODE'],
        value_vars=cs.numeric(),
        variable_name='employee_code',
        value_name='duration'
    )\
    .select(
        'employee_code',
        pl.col('JOB CODE').alias('project_code'),
        pl.lit(pendulum.parse('2024-03-01').date()).alias('month'),
        pl.col('duration').cast(pl.Float64)
    )
    
    
timesheet_april = pl.read_excel(file_name, sheet_name='April')\
    .melt(
        id_vars=['JOB CODE'],
        value_vars=cs.numeric(),
        variable_name='employee_code',
        value_name='duration'
    )\
    .select(
        'employee_code',
        pl.col('JOB CODE').alias('project_code'),
        pl.lit(pendulum.parse('2024-04-01').date()).alias('month'),
        pl.col('duration').cast(pl.Float64)
    )
    
timesheet_may = pl.read_excel(file_name, sheet_name='May')\
    .melt(
        id_vars=['JOB CODE'],
        value_vars=cs.numeric(),
        variable_name='employee_code',
        value_name='duration'
    )\
    .select(
        'employee_code',
        pl.col('JOB CODE').alias('project_code'),
        pl.lit(pendulum.parse('2024-05-01').date()).alias('month'),
        pl.col('duration').cast(pl.Float64)
    )


timesheet_df = pl.concat([timesheet_january, timesheet_february, timesheet_march, timesheet_april, timesheet_may])\
    .filter(pl.col('duration') > 0)
    
pandas_timesheet_df = timesheet_df.to_pandas()  
 
with pd.ExcelWriter(file_name, engine='openpyxl', mode='a' if os.path.exists(file_name) else 'w', if_sheet_exists='replace') as writer:
    pandas_timesheet_df.to_excel(writer, sheet_name='Combined', index=False)
    
print(timesheet_df)
#     .select(
#         pl.col('JOB CODE').alias('project_code'),
#         'employee_code',
#         'duration'
#     )\
#     .join(employee_df.select('employee_code'), on='employee_code')\
#     .join(project_df.select('project_code'), on='project_code')\
#     .with_columns(pl.lit(pendulum.parse('2024-01-01').date()).alias('month'))
    
    
# timesheet_february = pl.read_excel(file_name, sheet_name='timesheet_2024-02')\
#     .melt(
#         id_vars=['PROJECT NAME', 'JOB CODE'],
#         value_vars=cs.numeric(),
#         variable_name='employee_code',
#         value_name='duration'
#     )\
#     .select(
#         pl.col('JOB CODE').alias('project_code'),
#         'employee_code',
#         pl.col('duration').cast(pl.Float64)
#     )\
#     .join(employee_df.select('employee_code'), on='employee_code')\
#     .join(project_df.select('project_code'), on='project_code')\
#     .with_columns(pl.lit(pendulum.parse('2024-02-01').date()).alias('month'))

    
