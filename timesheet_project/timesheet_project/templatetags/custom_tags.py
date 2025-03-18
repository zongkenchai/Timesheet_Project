from django import template

register = template.Library()

@register.filter(name='user_in_group')
def user_in_group(user, group_string):
    
    return user.groups.filter(name__in=group_string.split(',')).exists() or user.is_superuser