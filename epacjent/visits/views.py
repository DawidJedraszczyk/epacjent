from django.shortcuts import render, get_object_or_404
from .forms import VisitForm, VisitDateForm, CancelVisitForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Visit
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

def checkAccess(host, user):
    if host != user:
        return HttpResponse('You are not allowed here!')


class Index(View):
    template_name = "visits.html"

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        user = request.user
        visits = Visit.objects.filter(user=user).order_by('visit_date', 'visit_hour')
        context = {'visits': visits}
        return render(request, self.template_name, context)

class VisitView(View):
    template_name = "singleVisit.html"

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk):
        visit = get_object_or_404(Visit, id=pk)
        context = {'visit': visit}
        return render(request, self.template_name, context)
class CreateVisitView(View):
    template_name = 'createVisit.html'
    form_class = VisitForm

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            visit_date_str = request.POST.get('visit_date')
            if visit_date_str:
                today = datetime.now().date()
                visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
                if visit_date < today:
                    messages.error(request, 'Invalid inputs')
                else:
                    Visit.objects.create(
                        user=request.user,
                        name=request.POST.get('name'),
                        description=request.POST.get('description'),
                        visit_date=request.POST.get('visit_date'),
                        visit_hour=request.POST.get('visit_hour'),
                    )
                    return HttpResponseRedirect(reverse('visits:visitsPanel'))
            else:
                Visit.objects.create(
                    user=request.user,
                    name=request.POST.get('name'),
                    description=request.POST.get('description'),
                )
                return HttpResponseRedirect(reverse('visits:visitsPanel'))

        context = {'form': form}
        return render(request, self.template_name, context)

class CancelVisitView(View):
    template_name = 'cancelVisit.html'
    form_class = CancelVisitForm

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk, *args, **kwargs):
        visit = get_object_or_404(Visit, id=pk)
        checkAccess(visit.user, request.user)
        form = self.form_class(instance=visit)
        context = {'form': form}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk, *args, **kwargs):
        visit = get_object_or_404(Visit, id=pk)
        checkAccess(visit.user, request.user)
        visit.delete()
        return HttpResponseRedirect(reverse('visits:visitsPanel'))


class UpdateVisitView(View):
    template_name = 'chooseDate.html'
    form_class = VisitDateForm

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk, *args, **kwargs):
        visit = get_object_or_404(Visit, id=pk)
        checkAccess(visit.user, request.user)
        form = self.form_class(instance=visit)
        context = {'form': form}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk, *args, **kwargs):
        visit = get_object_or_404(Visit, id=pk)
        checkAccess(visit.user, request.user)
        form = self.form_class(request.POST, instance=visit)
        if form.is_valid():
            today = datetime.now().date()
            visit_date_str = request.POST.get('visit_date')
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()

            if visit_date > today:
                visit.visit_date = visit_date
                visit.visit_hour = request.POST.get('visit_hour')
                visit.save()
                return HttpResponseRedirect(reverse('visits:visitsPanel'))
            else:
                messages.error(request, 'Invalid input')

        context = {'form': form}
        return render(request, self.template_name, context)