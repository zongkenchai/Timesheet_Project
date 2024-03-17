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

@permission_required('is_staff', raise_exception=True)
def update_dashboard(request):
    print(request, 'update')
    position_df = pl.from_records(Position.objects.all().values())
    employee_df = pl.from_records(Employee.objects.all().values())
    project_df = pl.from_records(Project.objects.all().values())
    company_df = pl.from_records(Company.objects.all().values())
    timesheet_df = pl.from_records(TimesheetLog.objects.all().values())
    payroll_df = pl.from_records(Payroll.objects.all().values())
    project_income_df = pl.from_records(ProjectIncome.objects.all().values())
    print(employee_df.columns)
    
    position_df = position_df\
        .rename({'id':'fk_position_id_id'})
        
    employee_df = employee_df\
        .join(position_df, on='fk_position_id_id')\
        .select(
            pl.col('id').alias('fk_employee_id_id'),
            'employee_id',
            pl.concat_str([pl.col('first_name'), pl.col('last_name')], separator=' ').alias('full_name'),
            'gender',
            'fk_position_id_id',
            'position',
            'department',
            'start_date',
            'end_date',
            (pl.when(pl.col('end_date').is_null()).then(pl.lit(1)).otherwise(pl.lit(0))).alias('active')
        )
    
    # print(employee_df)

    project_income_grouped_df = project_income_df\
        .group_by(
            'fk_project_id_id'
        )\
        .agg(
            pl.sum('amount').alias('total_paid')
        )
    company_df = company_df\
        .rename({'id':'fk_company_id_id'})
        
    project_df = project_df\
        .join(company_df, on='fk_company_id_id')\
        .select(
            pl.col('id').alias('fk_project_id_id'),
            'project_code',
            'project_name',
            'fk_company_id_id',
            'company_name',
            pl.col('start_date').alias('project_start_date'),
            pl.col('end_date').alias('project_end_date'),
            'expected_revenue'
        )\
        .join(project_income_grouped_df, on='fk_project_id_id', how='left')\
        .with_columns(
             pl.col('total_paid').fill_null(0.00)
        )\
        .with_columns(
            (pl.col('expected_revenue') - pl.col('total_paid')).alias('outstanding_balance')
        )
    
    
    payroll_df = payroll_df\
        .join(
            employee_df\
                .select(
                    'fk_employee_id_id',
                    'employee_id',
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
                    'employee_id',
                    'full_name',
                    'position',
                    'department',
                ),
            on='fk_employee_id_id'
        )\
        .join(
            project_df\
                .select(
                    'fk_project_id_id',
                    'project_code',
                    'project_name'
                ),
            on='fk_project_id_id'
        )\
        .with_columns(
            (pl.col('date').dt.truncate('1mo').alias('month')),
            (pl.col('duration') / (1000000 * 3600)).alias('duration'),
        )

    project_income_monthly = project_income_df\
        .groupby(
            'fk_project_id_id',
            pl.col('invoice_date').dt.truncate('1mo').alias('month')
        )\
        .agg(
            pl.sum('amount').alias('invoice_amount')   
        )
    
    timesheet_x_payroll = timesheet_df\
        .join(
            payroll_df\
                .select(
                    'fk_employee_id_id',
                    'month',
                    pl.col('amount').alias('payroll_amount')
                ), 
            on=['fk_employee_id_id', 'month'],
            how='left'
        )\
        .join(
            project_income_monthly
            ,
                on=['fk_project_id_id', 'month'],
                how='left'
        )\
        .with_columns(
            pl.col('duration').sum().over('fk_employee_id_id', 'month').alias('total_duration_employee'),
            
        )\
        .with_columns(
            ((pl.col('duration')/pl.col('total_duration_employee'))*pl.col('payroll_amount')).alias('cost')
        )
        
    
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
        .with_columns(
            (pl.col('total_cost')/pl.col('total_duration')).alias('cost_per_hour')
        )
        
    project_income_expense_monthly = project_income_monthly\
        .join(project_expense_monthly, on=['fk_project_id_id', 'month'], how='outer')\
        .with_columns(
            (pl.coalesce(['fk_project_id_id', 'fk_project_id_id_right'])).alias('fk_project_id_id'),
            (pl.coalesce(['month', 'month_right'])).alias('month'),
        )\
        .drop('fk_project_id_id_right', 'month_right')\
        .rename({'invoice_amount':'total_income'})\
        .with_columns(
            pl.col('total_income').fill_null(0.00),
            pl.col('total_employee').fill_null(0.00),
            pl.col('total_duration').fill_null(0.00),
            pl.col('total_cost').fill_null(0.00),
            pl.col('cost_per_hour').fill_null(0.00),
        )\
        .with_columns(
            (pl.col('total_income') - pl.col('total_cost')).alias('total_profit')
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
        
    
    gsheet_id = settings.GSHEET_ID
    gs = Gsheet()
    gs.update_data(worksheet_name='employee', df=employee_df.to_pandas())
    gs.update_data(worksheet_name='project', df=project_df.to_pandas())
    gs.update_data(worksheet_name='timesheet', df=timesheet_df.to_pandas())
    gs.update_data(worksheet_name='payroll', df=payroll_df.to_pandas())
    gs.update_data(worksheet_name='project_income', df=project_income_df.to_pandas())
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