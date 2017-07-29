from django.contrib import admin

from .models import Post, Employee, StructureUnit
from .models import BusinessProcess, Project

admin.site.register(Post)
admin.site.register(Employee)
admin.site.register(StructureUnit)
admin.site.register(BusinessProcess)
admin.site.register(Project)