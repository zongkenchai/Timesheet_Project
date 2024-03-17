import django_filters
from django_filters.widgets import RangeWidget
from .models import *
from position.models import *

def Titles():
    options = []
    for index,row in enumerate(Position.objects.values("position").distinct()):
        option = (str(row["position"]),str(row["position"]))
        options.append(option)
    return sorted(tuple(options),key=lambda x:x[0])


def Departments():
    options = []
    for index,row in enumerate(Position.objects.values("department").distinct()):
        option = (str(row["department"]),str(row["department"]))
        options.append(option)
    return sorted(tuple(options),key=lambda x:x[0])    
   

class EmployeeFilter(django_filters.FilterSet):
    employee_code = django_filters.CharFilter(lookup_expr="icontains", label='Employee ID')
    full_name = django_filters.CharFilter(lookup_expr="icontains", label='Full Name')
    email_address = django_filters.CharFilter(lookup_expr="icontains", label='Email Address')
    HAS_RESIGNED_CHOICES = [
        ('active', 'Active'),
        ('resigned', 'Resigned')   
    ]
    has_resigned = django_filters.ChoiceFilter(choices=HAS_RESIGNED_CHOICES, label='Active', method='search_has_resigned')
    title = django_filters.ChoiceFilter(choices=Titles, label='Title', method='search_title')
    department = django_filters.ChoiceFilter(choices=Departments, label='Department', method='search_department')
    
    def search_has_resigned(self, queryset, name, value):
        if value == 'active':
            has_resigned = Employee.objects.all().filter(Q(end_date__isnull=True))
        else:
            has_resigned = Employee.objects.all().filter(Q(end_date__isnull=False))
        return queryset.filter(employee_id__in=[i.employee_id for i in has_resigned])
    
    def search_title(self, queryset, name, value):
        position_list = Position.objects.all().filter(Q(title=value))
        employee_list = Employee.objects.all().filter(Q(fk_position_id__in=[i.id for i in position_list]))
        return queryset.filter(employee_id__in=[i.employee_id for i in employee_list])
    
    def search_department(self, queryset, name, value):
        position_list = Position.objects.all().filter(Q(department=value))
        employee_list = Employee.objects.all().filter(Q(fk_position_id__in=[i.id for i in position_list]))
        return queryset.filter(employee_id__in=[i.employee_id for i in employee_list])

    class Meta:
        model = Employee
        fields = ['employee_code', 'full_name', 'email_address', 'has_resigned', 'title', 'department']
