import sys, os
sys.path.append('./timesheet_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()


from django.contrib.auth.models import Group,Permission

staff_permission_list =  [
    'timesheet_log.view_timesheetlog',
    'timesheet_log.add_timesheetlog',
    'timesheet_log.change_timesheetlog',
    'timesheet_log.delete_timesheetlog',
    ]

manager_permisison_list = [
    'timesheet_log.view_timesheetlog',
    'timesheet_log.add_timesheetlog',
    'timesheet_log.change_timesheetlog',
    'timesheet_log.delete_timesheetlog',
    'project.view_project',
    'project.add_project',
    'project.change_project',
    'project.delete_project',
    'project.view_projectphase',
    'project.add_projectphase',
    'project.change_projectphase',
    'project.delete_projectphase',
    'project.view_projectphaseforecastrevenue',
    'project_income.add_projectinvoiceuploadfile',
    'project_income.view_projectinvoice',
    'project_income.add_projectinvoice',
    'project_income.change_projectinvoice',
    'project_income.delete_projectinvoice',
    # 'project_income.add_projectpaymentuploadfile',
    # 'project_income.view_projectpayment',
    # 'project_income.add_projectpayment',
    # 'project_income.change_projectpayment',
    # 'project_income.delete_projectpayment',
]


#Creating Researcher group
Staff, created_bool = Group.objects.get_or_create(name="Staff")
[Staff.permissions.add(Permission.objects.get(codename=permission.split(".")[1])) for permission in staff_permission_list]

Manager, created_bool = Group.objects.get_or_create(name="Manager")
[Manager.permissions.add(Permission.objects.get(codename=permission.split(".")[1])) for permission in manager_permisison_list]


