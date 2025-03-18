from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Creates Staff and Manager groups with appropriate permissions"

    def handle(self, *args, **kwargs):
        staff_permission_list = [
            "timesheet_log.view_timesheetlog",
            "timesheet_log.add_timesheetlog",
            "timesheet_log.change_timesheetlog",
            "timesheet_log.delete_timesheetlog",
        ]

        manager_permission_list = [
            "timesheet_log.view_timesheetlog",
            "timesheet_log.add_timesheetlog",
            "timesheet_log.change_timesheetlog",
            "timesheet_log.delete_timesheetlog",
            "project.view_project",
            "project.add_project",
            "project.change_project",
            "project.delete_project",
            "project.view_projectphase",
            "project.add_projectphase",
            "project.change_projectphase",
            "project.delete_projectphase",
            "project.view_projectphaseforecastrevenue",
            "project_income.add_projectinvoiceuploadfile",
            "project_income.view_projectinvoice",
            "project_income.add_projectinvoice",
            "project_income.change_projectinvoice",
            "project_income.delete_projectinvoice",
        ]

        # Creating or getting the Staff group
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        self.assign_permissions(staff_group, staff_permission_list)

        # Creating or getting the Manager group
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        self.assign_permissions(manager_group, manager_permission_list)

        self.stdout.write(self.style.SUCCESS("Successfully created/updated groups and permissions."))

    def assign_permissions(self, group, permissions_list):
        for perm in permissions_list:
            app_label, codename = perm.split(".")
            try:
                permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                group.permissions.add(permission)
            except ObjectDoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission '{perm}' not found. Skipping."))
