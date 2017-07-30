from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100)
    shortened_title = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.shortened_title or self.title

class Employee(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    post = models.ForeignKey(Post, related_name='+')
    is_head = models.BooleanField()
    default_deputy = models.ForeignKey('self', null=True, blank=True, related_name='+')
    deputy_by_order = models.ForeignKey('self', null=True, blank=True, related_name='+')
    branch = models.ForeignKey('StructureUnit', null=True, blank=True, related_name='+')
    
    user = models.OneToOneField(User, null=True, blank=True)

    def get_initials(self):
        return f'{self.last_name} {self.first_name[0]}. {self.patronymic[0]}.'
    def __str__(self):
        return self.get_initials()

class StructureUnit(TimeStampedModel):
    STRUCTURE_UNIT_TYPE = (
        (0, 'Department'),
        (1, 'Section'),
        (2, 'Team')
    )

    name = models.CharField(max_length=100)
    shortened_name = models.CharField(max_length=10)
    head = models.ForeignKey(Employee)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='+')
    type = models.PositiveSmallIntegerField(choices=STRUCTURE_UNIT_TYPE)

    def __str__(self):
        return self.shortened_name

class BusinessProcess(TimeStampedModel):
    title = models.CharField(max_length=30)
    short_title = models.CharField(max_length=10)
    manager = models.ForeignKey(Employee, related_name='+')
    exec = models.ForeignKey(Employee, related_name='+')

    def __str__(self):
        return self.title;

class Project(TimeStampedModel):
    code = models.CharField(max_length=15, unique=True)
    title= models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(Employee, related_name='+')
    exec = models.ForeignKey(Employee)
    openning_order_number = models.CharField(max_length=20)
    openning_order_date = models.DateField('openning order date')
    closure_act_number = models.CharField(max_length=20, null=True, blank=True)
    closure_act_date = models.DateField('closure act date', null=True, blank=True)
    completion_date = models.DateField('completion date', null=True, blank=True)
    plan = models.OneToOneField('Plan', blank=True)

    def __str__(self):
        return f'{self.code}. {self.title}';

class Plan(TimeStampedModel):
    WORK_TYPE_FOR_ORDER = 0
    WORK_TYPE_FOR_PROJECT = 1
    WORK_TYPE_FOR_BUSINESS_PROCESS = 2
    WORK_TYPE_FOR_MINUTES_OF_THE_MITING = 3
    WORK_TYPE_ARBITRARY = 4
    WORK_TYPES = (
        (WORK_TYPE_FOR_ORDER,    'For order'),
        (WORK_TYPE_FOR_PROJECT,    'For project'),
        (WORK_TYPE_FOR_BUSINESS_PROCESS,    'For business process'),
        (WORK_TYPE_FOR_MINUTES_OF_THE_MITING,    'For minutes of the meeting'),
        (WORK_TYPE_ARBITRARY,    'Arbitrary')
        )

    work_type = models.PositiveSmallIntegerField(choices=WORK_TYPES)
    business_process = models.ForeignKey(BusinessProcess)
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(Employee, null=True, blank=True)

    STATUS_PREPARED = 0
    STATUS_ON_AGREEMENT = 1
    STATUS_AGREED = 2
    STATUSES = (
        (STATUS_PREPARED, 'Prepared'),
        (STATUS_ON_AGREEMENT, 'On agreement'),
        (STATUS_AGREED, 'Agreed')
    )
    status = models.PositiveSmallIntegerField(choices=STATUSES)

    commentary = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField('Creation data')

@receiver(pre_save, sender=Project)
def create_plan_to_new_project(sender, instance, **kwargs):
    """Create Plan for every new Project."""
    if instance._state.adding is True:
        plan = Plan.objects.create(
            work_type=Plan.WORK_TYPE_FOR_PROJECT,
            business_process=instance.business_process,
            title=f'Plan for project {instance.code}',
            status=Plan.STATUS_PREPARED,
            creation_date=timezone.now())
        instance.plan = plan

class Task(TimeStampedModel):
    text = models.CharField(max_length=50)
    plan = models.ForeignKey(Plan)
    parent_task = models.ForeignKey('self')
    idx = models.PositiveIntegerField()
    labor_input_planned = models.PositiveIntegerField()
    duration_planned = models.FloatField()
    exec = models.ForeignKey(Employee)
    begin_planned = models.DateField('Planned start')
    end_planned = models.DateField('Planned finish')

    STATUS_PREPARED = 0
    STATUS_ON_AGREEMENT = 1
    STATUS_STOPPED = 2
    STATUS_IN_PROGRESS = 3
    STATUS_FINISHED = 4
    STATUSES = (
        (STATUS_PREPARED, 'Prepared'),
        (STATUS_ON_AGREEMENT, 'On agreement'),
        (STATUS_STOPPED, 'Stopped'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_FINISHED, 'Finished')
    )
    status = models.PositiveSmallIntegerField(choices=STATUSES)

    completeness = models.PositiveSmallIntegerField()
    prio = models.PositiveSmallIntegerField(default=0)
    labor_input_actual = models.PositiveIntegerField()
    duration_actual = models.FloatField()
    begin_actual = models.DateTimeField('Actual start date')
    end_actual = models.DateTimeField('Actual finish date')