from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.db.models import *
from django.db.models.functions import *
from django.conf import settings

from .models import *
from timesheet_log.models import *
from project_income.models import *
from employee.models import *
from project.models import *
from payroll.models import *
from company.models import *
from position.models import *

import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import polars as pl



class DashboardView(LoginRequiredMixin, TemplateView):
    #landing page view that features all main initial options
    #only require login + permission checks on front end to see which buttons can be accessed
    template_name = "dashboard_view.html"
    
    
# def dashboard_view(PermissionRequiredMixin, request):
#     # print(request)
#     return render(request, 'dashboard_view.html')

@permission_required('is_admin', raise_exception=True)
def update_dashboard(request):
    print(request, 'update')
    position_df = pl.from_records(Position.objects.all().values())
    department_df = pl.from_records(Department.objects.all().values())
    employee_df = pl.from_records(Employee.objects.all().values())
    project_df = pl.from_records(Project.objects.all().values())
    project_phase_df = pl.from_records(ProjectPhase.objects.all().values())
    company_df = pl.from_records(Company.objects.all().values())
    timesheet_df = pl.from_records(TimesheetLog.objects.all().values())
    payroll_df = pl.from_records(Payroll.objects.all().values())
    project_invoice_df = pl.from_records(ProjectInvoice.objects.all().values())
    project_payment_df = pl.from_records(ProjectPayment.objects.all().values())
    
    position_df = position_df\
        .rename({'id':'fk_position_id_id'})
        
    department_df = department_df\
        .rename(
            {
                'id': 'fk_department_id_id',
                'name': 'department'
            }
        )
    
    employee_df = employee_df\
        .join(position_df, on='fk_position_id_id')\
        .join(department_df, on='fk_department_id_id')\
        .select(
            pl.col('id').alias('fk_employee_id_id'),
            'staff_id',
            'employee_code',
            'full_name',
            'fk_position_id_id',
            'fk_department_id_id',
            'position',
            'department',
            'start_date',
            'end_date',
            (pl.when(pl.col('end_date').is_null()).then(pl.lit(1)).otherwise(pl.lit(0))).alias('active')
        )
    
    # print(employee_df)
    project_invoice_df = project_invoice_df\
        .rename({'id':'fk_invoice_id_id'})
        
    project_payment_grouped_df = project_payment_df\
        .join(
            project_invoice_df, on='fk_invoice_id_id'
        )\
        .group_by(
            'fk_project_id_id'
        )\
        .agg(
            pl.sum('amount').alias('total_paid')
        )

    project_invoice_payment_grouped_df = project_invoice_df\
        .group_by(
            'fk_project_id_id'
        )\
        .agg(
            pl.sum('amount').alias('total_invoice'),
        )\
        .join(project_payment_grouped_df, on='fk_project_id_id', how='left')\
        .with_columns(
             pl.col('total_invoice').fill_null(0.00),
             pl.col('total_paid').fill_null(0.00),
        )\
        .with_columns(
            (pl.col('total_invoice') - pl.col('total_paid')).alias('total_outstanding')
        )\
        .with_columns(
            pl.col('total_outstanding').fill_null(0.00),
        )
        
        
    project_phase_grouped_df = project_phase_df\
        .group_by('fk_project_id_id')\
        .agg(
            pl.sum('phase_fee').alias('total_fee'),
            pl.sum('phase_additional_fee').alias('total_additional_fee'),
            pl.sum('on_hold_fee').alias('total_on_hold_fee'),
            pl.sum('cancellation_fee').alias('total_cancellation_fee'),
        )


    
    company_df = company_df\
        .rename({'id':'fk_company_id_id'})
    
    project_df = project_df\
        .join(company_df, on='fk_company_id_id')\
        .join(employee_df.rename({'fk_employee_id_id':'fk_project_manager_id_id'}), on='fk_project_manager_id_id', how='left')\
        .select(
            pl.col('id').alias('fk_project_id_id'),
            'project_code',
            'project_name',
            'fk_company_id_id',
            pl.col('company_name').alias('customer'),
            pl.col('full_name').alias('project_manager'),
            pl.col('start_date').alias('project_start_date'),
            pl.col('end_date').alias('project_end_date'),
            'original_project_fee'
        )\
        .join(project_phase_grouped_df, on='fk_project_id_id', how='left')\
        .join(project_invoice_payment_grouped_df, on='fk_project_id_id', how='left')\
        .with_columns(
             pl.col('total_invoice').fill_null(0.00),
             pl.col('total_paid').fill_null(0.00),
             pl.col('total_outstanding').fill_null(0.00),
             pl.col('total_fee').fill_null(0.00),
             pl.col('total_additional_fee').fill_null(0.00),
             pl.col('total_on_hold_fee').fill_null(0.00),
             pl.col('total_cancellation_fee').fill_null(0.00),
        )
    print(project_df)
    
    
    payroll_df = payroll_df\
        .join(
            employee_df\
                .select(
                    'fk_employee_id_id',
                    'staff_id',
                    'employee_code',
                    'full_name',
                    'position',
                    'department',
                ),
            on='fk_employee_id_id')\
        .with_columns(
            (pl.col('date').dt.truncate('1mo').alias('month')),
        )
        
    
    timesheet_df = timesheet_df\
        .join(
            employee_df\
                .select(
                    'fk_employee_id_id',
                    'staff_id',
                    'employee_code',
                    'full_name',
                    'position',
                    'department',
                ),
            on='fk_employee_id_id', how='left'
        )\
        .join(
            project_df\
                .select(
                    'fk_project_id_id',
                    'project_code',
                    'project_name',
                    'customer',
                    'project_manager'
                ),
            on='fk_project_id_id', how='left'
        )\
        .with_columns(
            (pl.col('date').dt.truncate('1mo').alias('month')),
            (pl.col('duration')).alias('duration'),
        )
        
    project_payment_monthly_df = project_payment_df\
        .join(
            project_invoice_df, on='fk_invoice_id_id'
        )\
        .group_by(
            'fk_project_id_id',
            pl.col('payment_date').dt.truncate('1mo').alias('month')
        )\
        .agg(
            pl.sum('amount').alias('total_paid')
        )

    project_invoice_payment_monthly_df = project_invoice_df\
        .group_by(
            'fk_project_id_id',
            pl.col('invoice_date').dt.truncate('1mo').alias('month')

        )\
        .agg(
            pl.sum('amount').alias('total_invoice'),
        )\
        .join(project_payment_monthly_df, on=['fk_project_id_id', 'month'], how='outer')\
        .with_columns(
            (pl.coalesce(['fk_project_id_id', 'fk_project_id_id_right'])).alias('fk_project_id_id'),
            (pl.coalesce(['month', 'month_right'])).alias('month'),
             pl.col('total_invoice').fill_null(0.00),
             pl.col('total_paid').fill_null(0.00),
        )\
        .drop('fk_project_id_id_right', 'month_right')\
        .with_columns(
            (pl.col('total_invoice') - pl.col('total_paid')).alias('total_outstanding')
        )\
        .with_columns(
            pl.col('total_outstanding').fill_null(0.00),
        )
    
    print(project_invoice_payment_monthly_df.columns)
    timesheet_x_payroll = timesheet_df\
        .join(
            payroll_df\
                .select(
                    'fk_employee_id_id',
                    'month',
                    pl.col('amount').alias('payroll_amount')
                ), 
            on=['fk_employee_id_id', 'month'],
            how='outer'
        )\
        .with_columns(
            (pl.coalesce(['fk_employee_id_id', 'fk_employee_id_id_right'])).alias('fk_employee_id_id'),
            (pl.coalesce(['month', 'month_right'])).alias('month'),
             pl.col('payroll_amount').fill_null(0.00),
        )\
        .drop('fk_employee_id_id_right', 'month_right')\
        .join(
            project_invoice_payment_monthly_df,
                on=['fk_project_id_id', 'month'],
                how='left'
        )\
        .with_columns(
            pl.col('total_invoice').fill_null(0.00),
            pl.col('total_paid').fill_null(0.00),
            pl.col('total_outstanding').fill_null(0.00),
            pl.col('payroll_amount').fill_null(0.00)
        )\
        .filter(pl.col('duration') > 0)\
        .with_columns(
            pl.col('duration').sum().over('fk_employee_id_id', 'month').alias('total_duration_employee'),
        )\
        .with_columns(
            ((pl.col('duration')/pl.col('total_duration_employee'))*pl.col('payroll_amount')).alias('cost')
        )
        
    print(timesheet_x_payroll.columns)

    project_expense_monthly = timesheet_x_payroll\
        .groupby(
            'fk_project_id_id',
            'month'
        )\
        .agg(
            pl.n_unique('fk_employee_id_id').alias('total_employee'),
            pl.sum('duration').alias('total_duration'),
            pl.sum('cost').alias('total_cost')
        )\

        
    project_income_expense_monthly = project_invoice_payment_monthly_df\
        .join(project_expense_monthly, on=['fk_project_id_id', 'month'], how='outer')\
        .with_columns(
            (pl.coalesce(['fk_project_id_id', 'fk_project_id_id_right'])).alias('fk_project_id_id'),
            (pl.coalesce(['month', 'month_right'])).alias('month'),
        )\
        .drop('fk_project_id_id_right', 'month_right')\
        .with_columns(
            pl.col('total_invoice').fill_null(0.00),
            pl.col('total_paid').fill_null(0.00),
            pl.col('total_outstanding').fill_null(0.00),
            pl.col('total_employee').fill_null(0.00),
            pl.col('total_duration').fill_null(0.00),
            pl.col('total_cost').fill_null(0.00),
        )\
        .with_columns(
            (pl.col('total_invoice') - pl.col('total_cost')).alias('total_profit')
        )\
        .join(
            project_df\
                .select(
                    'fk_project_id_id',
                    'project_code',
                    'project_name'
                ),
            on='fk_project_id_id',
            how='left'
        )\
        
    
    employee_final_df = employee_df\
        .select(
            'staff_id',
            'employee_code',
            'full_name',
            'position',
            'department',
            'start_date',
            'end_date'
        )
    
    project_final_df = project_df\
        .select(
            'project_code',
            'project_name',
            'customer',
            'project_manager',
            'project_start_date',
            'project_end_date',
            'original_project_fee',
            'total_fee',
            'total_additional_fee',
            'total_on_hold_fee',
            'total_cancellation_fee',
            'total_invoice',
            'total_paid',
            'total_outstanding'
    )
    
    timesheet_final_df = timesheet_df\
        .select(
            'staff_id',
            'employee_code',
            'full_name',
            'position',
            'department',
            'project_code',
            'project_name',
            'customer',
            'project_manager',
            'date',
            'month',
            'duration'
        )
        
    payroll_final_df = payroll_df\
        .select(
            'staff_id',
            'employee_code',
            'full_name',
            'position',
            'department',
            pl.col('month').alias('payroll_month'),
            pl.col('amount').alias('payroll_amount')
        )
        
    print(project_income_expense_monthly)
    gsheet_id = settings.GSHEET_ID
    gs = Gsheet()
    gs.update_data(worksheet_name='employee', df=employee_final_df.to_pandas())
    gs.update_data(worksheet_name='project', df=project_final_df.to_pandas())
    gs.update_data(worksheet_name='timesheet', df=timesheet_final_df.to_pandas())
    gs.update_data(worksheet_name='payroll', df=payroll_final_df.to_pandas())
    gs.update_data(worksheet_name='project_invoice_payment', df=project_invoice_payment_monthly_df.to_pandas())
    gs.update_data(worksheet_name='timesheet_x_payroll', df=timesheet_x_payroll.to_pandas())
    gs.update_data(worksheet_name='project_income_expense', df=project_income_expense_monthly.to_pandas())
    
    return render(request, 'dashboard_view.html')



class Gsheet:
    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.google_auth_path = settings.GOOGLE_AUTH_PATH
        self.gsheet_id = settings.GSHEET_ID
        self.credentials = Credentials.from_service_account_file(self.google_auth_path, scopes=self.scopes)
        self.gc = gspread.authorize(self.credentials)
        self.gauth = GoogleAuth()
        self.drive = GoogleDrive(self.gauth)
        
    def update_data(self, **kwargs):
        worksheet_name = kwargs.get('worksheet_name')
        df = kwargs.get('df')
        gsheet = self.gc.open_by_key(self.gsheet_id)
        
        existing_worksheet_list = gsheet.worksheets()
        existing_worksheet_titles = [i.title for i in existing_worksheet_list]
        
        if worksheet_name not in existing_worksheet_titles:
            worksheet = gsheet.add_worksheet(worksheet_name, rows="100", cols="20")
        else:
            worksheet = gsheet.worksheet(worksheet_name)
            
        worksheet.clear()

        set_with_dataframe(
            worksheet=worksheet,
            dataframe=df,
            include_index=False,
            include_column_header=True,
            resize=False
        )