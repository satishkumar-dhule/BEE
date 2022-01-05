from django.forms import ModelForm
from django import forms

import caseapplication
from caseapplication.models import Case, Batch, Product, CustomBatch


class CaseForm(ModelForm):
    product = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    period = forms.MultipleChoiceField(choices=caseapplication.models.PERIOD_CHOICES)
    case_type = forms.MultipleChoiceField(choices=caseapplication.models.CASETYPE_CHOICES)

    class Meta:
        model = Case
        fields = ('product', 'period', 'case_type')


class BatchForm(ModelForm):
    cmd = forms.Textarea(attrs={'class': "form-control"})

    def __init__(self, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Batch
        fields = ('cmd',)

        def save(self, *args, **kwargs):
            kwargs['commit'] = False
            obj = super(BatchForm, self).save(*args, **kwargs)
            if self.request:
                obj.update_user_id = self.request.user
            obj.save()
            return obj


class CustomBatchForm(ModelForm):
    cmd_args = forms.Textarea(attrs={'class': "form-control"})

    def __init__(self, *args, **kwargs):
        super(CustomBatchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomBatch
        fields = ('cmd_args','target')

        def save(self, *args, **kwargs):
            kwargs['commit'] = False
            obj = super(CustomBatchForm, self).save(*args, **kwargs)
            if self.request:
                obj.update_user_id = self.request.user
            obj.save()
            return obj