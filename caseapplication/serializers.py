import django
from rest_framework import serializers
from .models import Case, Product, Batch, CustomBatch, Target


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('__all__')


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = django.contrib.auth.models.User
        fields = ('id','username')

class CustomBatchSerializerDisplay(serializers.ModelSerializer):
    target = TargetSerializer()
    add_user_id = UserSerializer()
    update_user_id = UserSerializer()

    class Meta:
        model = CustomBatch
        # fields = ('id', 'target',)
        # fields=('target_cmd','cmd_args','id','add_datetime','update_datetime','status','update_user_id','update_user_id')
        fields = ('__all__')


class CustomBatchSerializer(serializers.ModelSerializer):
    # target = TargetSerializer()

    class Meta:
        model = CustomBatch
        # fields = ('id', 'target',)
        # fields=('target_cmd','cmd_args','id','add_datetime','update_datetime','status','update_user_id','update_user_id')
        fields = ('__all__')

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ('__all__')

    # def get_case_type(self,instance):
    #     return instance.get_case_type_display()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['case_type_display'] = instance.get_case_type_display()
        data['add_user_name'] = instance.add_user_id.username
        if instance.update_user_id != None:
            data['update_user_name'] = instance.update_user_id.username
        else:
            data['update_user_name'] = 'None'
        data['product'] = instance.product.name
        from django.utils.timezone import timedelta
        from django.utils import timezone

        now = timezone.now()
        time_threshold = now - timedelta(hours=1)

        # print(data['product'],Product.objects.all().filter(name=data['product'])[0].id,count)
        count = Case.objects.all().filter(product=Product.objects.all().filter(name=data['product'])[0].id,
                                          period=data['period'],
                                          case_type=data['case_type'],
                                          status='E',
                                          update_datetime__gte=time_threshold).count()
        # print(data['product'], Product.objects.all().filter(name=data['product'])[0].id, count)

        if count != 0 and data['status'] == 'N':
            # data['cooldown'] = 'Y'
            # data['locked_status'] = 'L'
            data['status'] = 'L'
        else:
            pass
            # data['cooldown'] = 'N'
            # data['locked_status'] = 'N'
        return data
