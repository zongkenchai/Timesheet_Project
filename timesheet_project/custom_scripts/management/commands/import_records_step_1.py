import polars as pl
import polars.selectors as cs
import pendulum
import os
import django

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from position.models import Position
from department.models import Department
from employee.models import Employee
from company.models import Company
from project.models import Project, ProjectPhase
from project_income.models import ProjectInvoice, ProjectPayment
from payroll.models import Payroll
from timesheet_log.models import TimesheetLog

# Load Excel File
file_name = 'Datapoint needed.xlsx'

# Read Sheets
position_sheet = pl.read_excel(file_name, sheet_name='position')
employee_sheet = pl.read_excel(file_name, sheet_name='employee')
salary_record_sheet = pl.read_excel(file_name, sheet_name='salary_record')
company_sheet = pl.read_excel(file_name, sheet_name='customer')
project_cleaned_sheet = pl.read_excel(file_name, sheet_name='project_cleaned')
project_income_sheet = pl.read_excel(file_name, sheet_name='project_income')
project_payment_sheet = pl.read_excel(file_name, sheet_name='project_payment')
payroll_sheet = pl.read_excel(file_name, sheet_name='payroll')

# Process Department & Position Data
department_df = position_sheet.select('department').unique()
position_df = employee_sheet.filter(pl.col('Staff ID').is_not_null()).select('position').unique()

# Process Employee Data
employee_df = employee_sheet\
    .filter(pl.col('Staff ID').is_not_null())\
    .join(position_sheet.rename({'position_name': 'employee_code'}), on='employee_code', how='left')\
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

# Process Project Data
project_cleaned_sheet = project_cleaned_sheet.with_columns(
    pl.col('project_start_date').str.to_date(format='%d %b %Y', strict=False),
    pl.col('project_end_date').str.to_date(format='%d %b %Y', strict=False),
    pl.col('phase_start_date').str.to_date(format='%d %b %Y', strict=False),
    pl.col('phase_end_date').str.to_date(format='%d %b %Y', strict=False),
)

company_df = project_cleaned_sheet.select('company_name').unique()

project_df = project_cleaned_sheet.group_by(
    'project_code', 'project_name', 'project_manager',
    'project_start_date', 'project_end_date', 'company_name'
).agg(pl.sum('Original_project_fee').alias('original_project_fee'))

project_phase_df = project_cleaned_sheet.select(
    'project_code', 'phase_name', 'phase_start_date', 'phase_end_date',
    pl.col('project_status').alias('phase_status'),
    pl.col('Original_project_fee').alias('phase_fee'),
    pl.col('Additional_fee').alias('phase_additional_fee'),
    pl.col('On-Hold_FEE').alias('on_hold_fee'),
    pl.col('Termination/ Cancellation FEE').alias('cancellation_fee'),
    pl.col('notes').alias('notes')
).with_columns(
    pl.col('phase_fee').fill_null(0.00),
    pl.col('phase_additional_fee').fill_null(0.00),
    pl.col('on_hold_fee').fill_null(0.00),
    pl.col('cancellation_fee').fill_null(0.00),
)

# Load Positions and Departments
Position.objects.bulk_create([Position(position=row["position"]) for row in position_df.iter_rows(named=True)])
Department.objects.bulk_create([Department(name=row["department"]) for row in department_df.iter_rows(named=True)])

# Load Employees
position_dict = {pos.position: pos for pos in Position.objects.all()}
department_dict = {dept.name: dept for dept in Department.objects.all()}

Employee.objects.bulk_create([
    Employee(
        staff_id=row['staff_id'],
        employee_code=row['employee_code'],
        full_name=row['full_name'],
        fk_position=position_dict.get(row['position']),
        fk_department=department_dict.get(row['department']),
        email_address=row['email_address'],
        start_date=row['start_date'],
        end_date=row['end_date']
    ) for row in employee_df.iter_rows(named=True)
])

# Load Companies
Company.objects.bulk_create([Company(company_name=row['company_name']) for row in company_df.iter_rows(named=True)])

# Load Projects
employee_dict = {emp.employee_code: emp for emp in Employee.objects.all()}
company_dict = {comp.company_name: comp for comp in Company.objects.all()}

Project.objects.bulk_create([
    Project(
        project_code=row['project_code'],
        project_name=row['project_name'],
        fk_project_manager=employee_dict.get(row['project_manager']),
        fk_company=company_dict.get(row['company_name']),
        start_date=row['project_start_date'],
        end_date=row['project_end_date'],
        original_project_fee=row['original_project_fee']
    ) for row in project_df.iter_rows(named=True)
])

# Load Project Phases
phase_status_dict = {
    'pre_tender': 'Pre-Tender',
    'construction': 'Construction',
    'on_hold': 'On Hold',
    'final_fee_to_collect': 'Final Fee to collect',
    'completed': 'Completed',
    'adhoc': 'Ad-hoc'
}

phase_status_df = pl.DataFrame({'phase_status_final': phase_status_dict.keys(), 'phase_status': phase_status_dict.values()})
project_phase_final_df = project_phase_df.join(phase_status_df, on='phase_status', how='left')

project_dict = {proj.project_code: proj for proj in Project.objects.all()}

ProjectPhase.objects.bulk_create([
    ProjectPhase(
        fk_project=project_dict.get(row['project_code']),
        phase_name=row['phase_name'],
        phase_start_date=row['phase_start_date'],
        phase_end_date=row['phase_end_date'],
        phase_status=row['phase_status_final'],
        phase_fee=row['phase_fee'],
        phase_additional_fee=row['phase_additional_fee'],
        on_hold_fee=row['on_hold_fee'],
        cancellation_fee=row['cancellation_fee'],
        notes=row['notes']
    ) for row in project_phase_final_df.iter_rows(named=True)
])

# Load Invoices
project_invoice_df = project_income_sheet.filter(pl.col('invoice_no').is_not_null()).with_columns(
    pl.col('invoice_date').str.replace_all('"', '').str.to_date(format='%d/%m/%Y', strict=False),
    pl.when(pl.col('is_cancelled') == 'No').then(pl.lit('no')).otherwise(pl.lit('yes')).alias('is_cancelled')
).rename({'amount_exclude_SST': 'amount'}).join(project_df, on='project_code')

ProjectInvoice.objects.bulk_create([
    ProjectInvoice(
        invoice_no=row['invoice_no'],
        invoice_date=row['invoice_date'],
        fk_project=project_dict.get(row['project_code']),
        amount=row['amount'],
        is_cancelled=row['is_cancelled']
    ) for row in project_invoice_df.iter_rows(named=True)
])

# Load Payments
invoice_dict = {inv.invoice_no: inv for inv in ProjectInvoice.objects.all()}
project_payment_df = project_payment_sheet.filter(pl.col('invoice_no').is_not_null()).with_columns(
    pl.col('payment_date').str.replace_all('"', '').str.to_date(format='%d-%m-%Y', strict=False),
).rename({'payment_exclude SST': 'amount'})

ProjectPayment.objects.bulk_create([
    ProjectPayment(
        fk_invoice=invoice_dict.get(row['invoice_no']),
        payment_no=row['payment_no'],
        payment_date=row['payment_date'],
        amount=row['amount']
    ) for row in project_payment_df.iter_rows(named=True)
])

# Load Payroll
Payroll.objects.bulk_create([
    Payroll(
        fk_employee=employee_dict.get(row['employee_code']),
        date=row['payroll_month'],
        amount=row['amount']
    ) for row in payroll_sheet.iter_rows(named=True)
])

print("Data successfully loaded into Django models.")
