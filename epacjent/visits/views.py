from django.shortcuts import render, redirect, get_object_or_404
from .forms import VisitForm, VisitDateForm
from .models import Visit
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse

def index(request):
    user = request.user
    visits = Visit.objects.filter(user=user).order_by('visit_date', 'visit_hour')
    context = {'visits': visits}
    return render(request, 'visits.html', context)

def visit(request, pk):
    visit = get_object_or_404(Visit, id=pk)
    context = {'visit': visit}
    return render(request, 'singleVisit.html', context)

def createVisit(request):
    form = VisitForm()
    if request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            visit_date_str = request.POST.get('visit_date')
            if visit_date_str:
                today = datetime.now().date()
                visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
                if visit_date < today:
                    messages.error(request, 'valid inputs')
                else:
                    Visit.objects.create(
                        user=request.user,
                        name = request.POST.get('name'),
                        description = request.POST.get('description'),
                        visit_date = request.POST.get('visit_date'),
                        visit_hour = request.POST.get('visit_hour'),
                    )
                    return redirect('visitsPanel')
            else:
                Visit.objects.create(
                    user=request.user,
                    name=request.POST.get('name'),
                    description=request.POST.get('description'),
                )
                return redirect('visitsPanel')
    context = {'form': form}
    return render(request, 'createVisit.html', context)


def updateVisit(request, pk):
    visit = get_object_or_404(Visit, id=pk)
    if request.user != visit.user:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        form = VisitDateForm(request.POST, instance=visit)
        if form.is_valid():
            today = datetime.now().date()
            visit_date_str = request.POST.get('visit_date')
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()

            if visit_date > today:
                visit.visit_date = visit_date
                visit.visit_hour = request.POST.get('visit_hour')
                visit.save()
                return redirect('visitsPanel')
            else:
                messages.error(request, 'Invalid input')
    else:
        form = VisitDateForm(instance=visit)

    context = {'form': form}
    return render(request, 'chooseDate.html', context)