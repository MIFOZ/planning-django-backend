from django.shortcuts import render
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.views import generic

from .models import Project, Plan, Task

def projects(request):
    """Renders the page with user projects."""
    assert isinstance(request, HttpRequest)

    employee = request.user.employee
    employees_in_projects = Project.objects.filter(

    )
    user_projects = Project.objects.filter(
        Q(manager=employee) |
        Q(exec=employee) |
        Q(plan__in=[plan for task in Task.objects.all()])
    )

    return render(
        request,
        'app/projects.html',
        {
            'title':'Projects',
            'year':datetime.now().year,
            'user_projects': user_projects
        }
    )

def plans(request):
    """Renders the page with plans created by user."""
    assert isinstance(request, HttpRequest)

    employee = request.user.employee
    user_plans = Plan.objects.filter(
        created_by=employee
    )

    return render(
        request,
        'app/plans.html',
        {
            'title':'Plans',
            'year':datetime.now().year,
            'user_plans': user_plans,
            'employee': employee,
            'user_can_create_plans': employee.is_head
        }
    )

def create_plan(reqeust):
    return HttpResponseRedirect(reverse('plans'))

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
