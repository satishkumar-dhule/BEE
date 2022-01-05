from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import *

PERIOD_CHOICES = []
PRODUCT_CHOICES = (('FX', 'FX'), ('EQ', 'EQ'))
STATUS_CHOICES = (
('N', 'NEW'), ('P', 'PROGRESSING'), ('E', 'ENDED OK'), ('F', 'FAILED'), ('L', 'LOCKED'), ('T', 'TERMINATED'))
CASETYPE_CHOICES = (
('A', 'CASE 1 - ManualAccrualToAlocation'), ('B', 'CASE 2 - Postings'), ('C', 'CASE 3 - InvoiceLineDetail'),
('E', 'CASE 5 -  InvoicePaymentPosting'))
ACTIVE_IND_CHOICES = (('Y', 'Y'), ('N', 'N'))

date = datetime.now()
for i in range(1, 37):
    v = (date + relativedelta(months=-i)).strftime('%m-%Y')
    PERIOD_CHOICES.append((v, v))


class CaseQuerySet(models.QuerySet):

    # results = Widget.objects.filter(created__lt=time_threshold)
    def myCases(self, user):
        # if user.is_superuser:
        # return self
        return self  # allows all users to see all case runs
        from datetime import datetime, timedelta
        time_threshold = datetime.now() - timedelta(hours=5)
        return self.filter(models.Q(update_datetime__gt=time_threshold))




class Product(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Case(models.Model):
    # product = models.CharField(max_length=10, choices=PRODUCT_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='case_product')
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    case_type = models.CharField(max_length=1, choices=CASETYPE_CHOICES)
    add_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    add_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ref_add_user_id')
    update_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ref_update_user_id', null=True,
                                       blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    record_active_ind = models.CharField(max_length=1, choices=ACTIVE_IND_CHOICES, default='Y')
    objects = CaseQuerySet.as_manager()

    # def save_model(self, request, obj, form, change):
    #     obj.update_user_id = request.user
    #     super().save_model(request, obj, form, change)
    #     obj.update_user_id = request.user
    #     obj.save()


class Batch(models.Model):
    cmd = models.TextField(max_length=1000, )
    add_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    add_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ref_batch_add_user_id')
    update_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ref_batch_update_user_id',
                                       null=True,
                                       blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    record_active_ind = models.CharField(max_length=1, choices=ACTIVE_IND_CHOICES, default='Y')


class Target(models.Model):
    host = models.CharField(max_length=30)
    cmd = models.TextField(max_length=1000)
    name = models.CharField(max_length=30, )

    def __str__(self):
        return self.name+'@'+self.host

    def __repr__(self):
        return self.name+'@'+self.host


class CustomBatch(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='ref_target')
    cmd_args = models.TextField(max_length=1000, )

    add_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    add_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ref_batch_add_user_id_custom_batch')
    update_user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name='ref_batch_update_user_id_custom_batch', null=True,
                                       blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    record_active_ind = models.CharField(max_length=1, choices=ACTIVE_IND_CHOICES, default='Y')

    def __str__(self):
        return str(self.id)+'@'+self.target.host

    def __repr__(self):
        return str(self.id)+'@'+self.target.host
