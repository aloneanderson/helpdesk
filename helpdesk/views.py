from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from .models import Requisitions, Comment
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RequisitionsCreateForm, RequisitionsUpdateForm, AcceptRequisitionsForm, CommentForm, \
    CancelRequisitionsForm, RecoveryRequisitionsForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin


class RegistrationUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('index')


class MyLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


class MyUserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class UserPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user


class RequisitionsView(ListView):
    model = Requisitions
    template_name = 'index.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                return Requisitions.objects.filter(user=self.request.user)
            return Requisitions.objects.all().filter(active_status=True)


class RequisitionsListView(ListView):
    model = Requisitions
    template_name = 'requisitions_list.html'


class RequisitionsCreateView(CreateView):
    model = Requisitions
    form_class = RequisitionsCreateForm
    template_name = 'create_requisitions.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        return super().form_valid(form=form)


class RequisitionsUpdateView(UserPermission, UpdateView):
    model = Requisitions
    template_name = 'requisitions_update.html'
    success_url = reverse_lazy('index')
    form_class = RequisitionsUpdateForm


class CommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        requisitions = Requisitions.objects.get(id=self.kwargs['pk'])
        if requisitions.active_status is False:
            raise Exception('You can''t add comment')
        object.requisitions = requisitions
        object.save()
        return super().form_valid(form=form)


class AcceptRequisitionsView(UpdateView):
    model = Requisitions
    success_url = reverse_lazy('index')
    template_name = 'requisitions_accept.html'
    form_class = AcceptRequisitionsForm

    def form_valid(self, form):
        if self.get_object().review is False:
            messages.error(self.request, 'Requisition CANCELED')
            return redirect('/')
        else:
            object = form.save(commit=False)
            object.review = True
        return super().form_valid(form=form)


class CancelRequisitionsView(CreateView):
    model = Comment
    success_url = reverse_lazy('index')
    template_name = 'requisitions_cancel.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        requisitions = Requisitions.objects.get(id=pk)
        if requisitions.review is False:
            messages.error(request, 'Requisition CANCELED')
            return redirect('/')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        requisitions = Requisitions.objects.get(id=pk)
        object = form.save(commit=False)
        object.requisitions = requisitions
        object.user = self.request.user
        requisitions.review = False
        requisitions.save()
        return super().form_valid(form=form)


class RecoveryRequisitionsView(UpdateView):
    model = Requisitions
    success_url = reverse_lazy('index')
    template_name = 'requisitions_recovery.html'
    form_class = RecoveryRequisitionsForm

    def form_valid(self, form):
        pk = self.kwargs['pk']
        requisitions = Requisitions.objects.get(id=pk)
        object = form.save(commit=False)
        object.requisitions = requisitions
        object.user = self.request.user
        requisitions.recovery = True
        requisitions.save()
        return super().form_valid(form=form)


class AdminRecoveryRequisitionsView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    model = Requisitions
    template_name = 'admin_requisitions_recovery.html'
    context_object_name = 'requisitions'


class AdminAcceptRecoveryRequisitionsView(UpdateView):
    model = Requisitions
    success_url = reverse_lazy('index')
    template_name = 'admin_requisitions_accept_recovery.html'
    form_class = AcceptRequisitionsForm

    def form_valid(self, form):
        pk = self.kwargs['pk']
        requisitions = Requisitions.objects.get(id=pk)
        object = form.save(commit=False)
        object.requisitions = requisitions
        object.user = self.request.user
        requisitions.review = True
        requisitions.active_status = False
        requisitions.save()
        return super().form_valid(form=form)


class AdminCancelRecoveryRequisitionsView(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_superuser'
    model = Requisitions
    success_url = reverse_lazy('index')
    template_name = 'admin_requisitions_cancel_recovery.html'
