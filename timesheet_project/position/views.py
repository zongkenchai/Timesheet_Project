from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from .models import *
from .forms import *

#! Position Main View
#TODO : Add sorting, permissions
class PositionListView(PermissionRequiredMixin, ListView):
    template_name = 'position_view.html'
    model = Position
    permission_required = 'position.view_position'
    context_object_name = 'position'
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     return filter.qs
    
    # def get_context_data(self, **kwargs):
    #     context = super(EmployeeListView, self).get_context_data(**kwargs)
    #     queryset = self.get_queryset()
    #     filter = EmployeeFilter(self.request.GET, queryset)
    #     context["position_filter"] = filter
    #     return context


class PositionCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'position_form.html'
    form_class = PositionForm
    model = Position
    permission_required = 'position.add_position'
    success_message = "Successfully Created Position"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('position_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class PositionUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'position_form.html'
    form_class = PositionForm
    model = Position
    permission_required = 'position.chnage_position'
    success_message = "Successfully Updated Position"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('position_list') # kwargs = {'pk':self.object.id}

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@permission_required('position.delete_position', raise_exception=True)
def delete_position(request, pk):
    if request.method=="GET":
        position = Position.objects.get(id=pk)
        messages.error(request, f"Successfully deleted {position.title}")
        position.delete()
        return HttpResponseRedirect(reverse('position_list'))