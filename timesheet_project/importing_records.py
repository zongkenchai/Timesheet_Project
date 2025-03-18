import polars as pl
file_name = 'Datapoint needed.xlsx'
position_sheet = pl.read_excel(file_name, sheet_name='position')
employee_sheet = pl.read_excel(file_name, sheet_name='employee')
salary_record_sheeet = pl.read_excel(file_name, sheet_name='salary_record')

department_df = position_sheet\
    .select('department')\
    .unique()
    
position_df = employee_sheet\
    .filter(
        pl.col('Staff ID').is_not_null()
    )\
    .select('position')\
    .unique()

employee_df = employee_sheet\
    .filter(
        pl.col('Staff ID').is_not_null()
    )\
    .join(
        position_sheet.rename({'position_name':'employee_code'}),
        on='employee_code', how='left'
    )\
    .select(
        pl.col('Staff ID').alias('staff_id'),
        'employee_code',
        pl.col('last_name').alias('full_name'),
        'position',
        'department',
        'email_address',
        pl.col('start_date').str.replace_all('"', '').str.to_date(format='%Y-%m-%d', strict=False),
        pl.col('end_date').str.replace_all('"', '').str.to_date(format='%Y-%m-%d', strict=False),
    )

company_sheet = pl.read_excel(file_name, sheet_name='customer')


project_cleaned_sheet = pl.read_excel(file_name, sheet_name='project_cleaned')\
    .with_columns(
        pl.col('project_start_date').str.to_date(format='%d %b %Y', strict=False),
        pl.col('project_end_date').str.to_date(format='%d %b %Y', strict=False),
        pl.col('phase_start_date').str.to_date(format='%d %b %Y', strict=False),
        pl.col('phase_end_date').str.to_date(format='%d %b %Y', strict=False),
    )
    
    
company_df = project_cleaned_sheet\
    .select(
        'company_name'
    )\
    .unique()

project_df = project_cleaned_sheet\
    .group_by(
        'project_code',
        'project_name',
        'project_manager',
        'project_start_date',
        'project_end_date',
        'company_name',
    )\
    .agg(pl.sum('Original_project_fee').alias('original_project_fee'))
    
    
project_phase_df = project_cleaned_sheet\
    .select(
        'project_code',
        'phase_name',
        'phase_start_date',
        'phase_end_date',
        pl.col('project_status').alias('phase_status'),
        pl.col('Original_project_fee').alias('phase_fee'),
        pl.col('Additional_fee').alias('phase_additional_fee'),
        pl.col('On-Hold_FEE').alias('on_hold_fee'),
        pl.col('Termination/ Cancellation FEE').alias('cancellation_fee'),
        pl.col('notes').alias('notes')
    )\
    .with_columns(
        pl.col('phase_fee').fill_null(0.00),
        pl.col('phase_additional_fee').fill_null(0.00),
        pl.col('on_hold_fee').fill_null(0.00),
        pl.col('cancellation_fee').fill_null(0.00),
    )
        
        

project_income_sheet = pl.read_excel(file_name, sheet_name='project_income')

project_invoice_df = project_income_sheet\
    .filter(pl.col('invoice_no').is_not_null())\
    .with_columns(
        pl.col('invoice_date').str.replace_all('"', '').str.to_date(format='%d/%m/%Y', strict=False),
        pl.when(pl.col('is_cancelled') == 'No').then(pl.lit('no')).otherwise(pl.lit('yes')).alias('is_cancelled')
    )\
    .rename({'amount_exclude_SST' : 'amount'})
    


project_payment_sheet = pl.read_excel(file_name, sheet_name='project_payment')
project_payment_df = project_payment_sheet\
    .filter(pl.col('invoice_no').is_not_null())\
    .with_columns(
        pl.col('payment_date').str.replace_all('"', '').str.to_date(format='%d-%m-%Y', strict=False),
    )\
    .rename({'payment_exclude SST':'amount'})


payroll_sheet = pl.read_excel(file_name, sheet_name='payroll')

payroll_df = payroll_sheet\
    .filter(pl.col('employee_code').is_not_null())\
    .with_columns(
        pl.col('payroll_month').str.replace_all('"', '').str.to_date(format='%Y-%m', strict=False),
    )
    
import polars.selectors as cs
import pendulum
timesheet_january = pl.read_excel(file_name, sheet_name='timesheet_2024-01')\
    .melt(
        id_vars=['PROJECT NAME', 'JOB CODE'],
        value_vars=cs.numeric(),
        variable_name='employee_code',
        value_name='duration'
    )\
    .select(
        pl.col('JOB CODE').alias('project_code'),
        'employee_code',
        'duration'
    )\
    .join(employee_df.select('employee_code'), on='employee_code')\
    .join(project_df.select('project_code'), on='project_code')\
    .with_columns(pl.lit(pendulum.parse('2024-01-01').date()).alias('month'))
    
    
timesheet_february = pl.read_excel(file_name, sheet_name='timesheet_2024-02')\
    .melt(
        id_vars=['PROJECT NAME', 'JOB CODE'],
        value_vars=cs.numeric(),
        variable_name='employee_code',
        value_name='duration'
    )\
    .select(
        pl.col('JOB CODE').alias('project_code'),
        'employee_code',
        pl.col('duration').cast(pl.Float64)
    )\
    .join(employee_df.select('employee_code'), on='employee_code')\
    .join(project_df.select('project_code'), on='project_code')\
    .with_columns(pl.lit(pendulum.parse('2024-02-01').date()).alias('month'))

    
timesheet_df = pl.concat([timesheet_january, timesheet_february])\
    .filter(pl.col('duration') > 0)
    
    
import csv
import sys, os
sys.path.append('./timesheet_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()


from position.models import *
from department.models import *
from employee.models import *
from company.models import *
from project.models import *
from project_income.models import *
from payroll.models import *
from timesheet_log.models import *

for row in position_df.iter_rows(named=True):
    Position.objects.create(
        position = row["position"],
    )
    
    
for row in department_df.iter_rows(named=True):
    Department.objects.create(
        name = row['department']
    )
    
for row in employee_df.iter_rows(named=True):
    Employee.objects.create(
        staff_id = row['staff_id'],
        employee_code = row['employee_code'],
        full_name = row['full_name'],
        fk_position_id = Position.objects.get(position=row['position']),
        fk_department_id = Department.objects.get(name=row['department']),
        email_address = row['email_address'],
        start_date = row['start_date'],
        end_date = row['end_date']
    )
    
for row in company_df.iter_rows(named=True):
    Company.objects.create(
        company_name = row['company_name']
    )
    
for row in project_df.iter_rows(named=True):
    print(row)
    Project.objects.create(
        project_code = row['project_code'],
        project_name = row['project_name'],
        fk_project_manager_id = Employee.objects.get(employee_code=row['project_manager']),
        fk_company_id = Company.objects.get(company_name=row['company_name']),
        start_date = row['project_start_date'],
        end_date = row['project_end_date'],
        original_project_fee = row['original_project_fee']
    )

phase_status_dictionary =    {
    'pre_tender':'Pre-Tender',
    'construction':'Construction',
    'on_hold':'On Hold',
    'final_fee_to_collect':'Final Fee to collect',
    'completed':'Completed',
    'adhoc': 'Ad-hoc'
}


# Combine Series into a DataFrame
phase_status_dictionary_df = pl.DataFrame(
    {'phase_status_final':phase_status_dictionary.keys(),
     'phase_status':phase_status_dictionary.values()}
    )

project_phase_final_df = project_phase_df\
    .join(phase_status_dictionary_df, on='phase_status', how='left')
    
for row in project_phase_final_df.iter_rows(named=True):
    ProjectPhase.objects.create(
        fk_project_id = Project.objects.get(project_code=row['project_code']),
        phase_name = row['phase_name'],
        phase_start_date = row['phase_start_date'],
        phase_end_date = row['phase_end_date'],
        phase_status = row['phase_status_final'],
        phase_fee = row['phase_fee'],
        phase_additional_fee = row['phase_additional_fee'],
        on_hold_fee = row['on_hold_fee'],
        cancellation_fee = row['cancellation_fee'],
        notes = row['notes'],
    )

project_invoice_df = project_invoice_df\
    .join(project_df, on='project_code')

for row in project_invoice_df.iter_rows(named=True):
    ProjectInvoice.objects.create(
        invoice_no = row['invoice_no'],
        invoice_date = row['invoice_date'],
        fk_project_id = Project.objects.get(project_code=row['project_code']),
        amount = row['amount'],
        is_cancelled = row['is_cancelled']
    )
    
    
for row in project_payment_df.iter_rows(named=True):
    ProjectPayment.objects.create(
        fk_invoice_id = ProjectInvoice.objects.get(invoice_no=row['invoice_no']),
        payment_no = row['payment_no'],
        payment_date = row['payment_date'],
        amount = row['amount']
        )


for row in payroll_df.iter_rows(named=True):
    Payroll.objects.create(
        fk_employee_id = Employee.objects.get(employee_code=row['employee_code']),
        date = row['payroll_month'],
        amount = row['amount']
    )
    
for row in timesheet_df.iter_rows(named=True):
    TimesheetLog.objects.create(
        fk_employee_id = Employee.objects.get(employee_code=row['employee_code']),
        fk_project_id = Project.objects.get(project_code = row['project_code']),
        date = row['month'],
        duration = row['duration']
    )