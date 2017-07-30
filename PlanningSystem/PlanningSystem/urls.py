"""
Definition of urls for PlanningSystem.
"""

from datetime import datetime
from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.projects, name='projects'),
    url(r'^plans', app.views.plans, name='plans'),
    url(r'create_plan$', app.views.create_plan, name='create_plan'),
    url(r'edit_plan$', app.views.edit_plan, name='edit_plan'),
    url(r'create_task', app.views.create_task, name='create_task'),
    url(r'^about', app.views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
