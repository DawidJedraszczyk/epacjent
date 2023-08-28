from django.shortcuts import render, redirect, get_object_or_404
from .forms import VisitForm
from .models import Visit
from datetime import datetime
from django.contrib import messages

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
            today = datetime.now().date()
            visit_date_str = visit_date = request.POST.get('visit_date')
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
            if visit_date > today:
                Visit.objects.create(
                    user=request.user,
                    name = request.POST.get('name'),
                    description = request.POST.get('description'),
                    visit_date = request.POST.get('visit_date'),
                    visit_hour = request.POST.get('visit_hour'),
                )
                return redirect('visitsPanel')
            else:
                messages.error(request, 'valid inputs')
    context = {'form': form}
    return render(request, 'createVisit.html', context)