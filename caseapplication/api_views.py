from _ast import List

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from caseapplication.serializers import CaseSerializer, BatchSerializer, CustomBatchSerializer, \
    CustomBatchSerializerDisplay
from .decorators import allowed_users
from .models import Case, Batch, CustomBatch
from django_filters.rest_framework import DjangoFilterBackend  # , IsOwnerOrSuperuser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

class CasePagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class BatchList(ListAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('id', 'status',)
    pagination_class = CasePagination
    ordering_fields = ['id', ]
    ordering = ['-id']

    def get_queryset(self):
        queryset = Batch.objects.all()
        return queryset


class CustomBatchList(ListAPIView):
    queryset = CustomBatch.objects.all()
    serializer_class = CustomBatchSerializerDisplay
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('id', 'status','target__host')
    pagination_class = CasePagination
    ordering_fields = ['id', ]
    ordering = ['-id']

    def get_queryset(self):
        queryset = CustomBatch.objects.all()
        return queryset


class CaseList(ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('id', 'status', 'product', 'case_type')
    pagination_class = CasePagination
    ordering_fields = ['id', 'case_type']
    ordering = ['-id']

    def get_queryset(self):
        eligible = self.request.query_params.get('eligible', None)
        queryset = Case.objects.all()
        if eligible is None:
            return queryset

        if eligible.lower() == "true":
            from django.utils import timezone
            stamp = timezone.now() - timezone.timedelta(hours=1)
            queryset = Case.objects.raw(
                "select id from caseapplication_case where  status ='N' and (product_id,period,case_type) not in  (select product_id,period,case_type  from  caseapplication_case where datetime(update_datetime) >=datetime('now', '-1 Hour') and status='E')")
            return Case.objects.filter(id__in=[x.id for x in queryset])

        return queryset


class CaseCreate(CreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class BatchCreate(CreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CustomBatchCreate(CreateAPIView):
    queryset = CustomBatch.objects.all()
    serializer_class = CustomBatchSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CaseDestroy(DestroyAPIView):
    get_queryset = CaseList.get_queryset
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        case_id = request.data.get(id)
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete("case_data_{}".format(case_id))


class BatchDestroy(DestroyAPIView):
    get_queryset = BatchList.get_queryset
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        batch_id = request.data.get(id)
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete("batch_data_{}".format(batch_id))


@allowed_users(['IT'])
class CutomBatchDestroy(DestroyAPIView):
    get_queryset = CustomBatchList.get_queryset
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        batch_id = request.data.get(id)
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete("batch_data_{}".format(batch_id))

from rest_framework.permissions import IsAdminUser


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CaseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)
    get_queryset = CaseList.get_queryset
    lookup_field = 'id'
    serializer_class = CaseSerializer

    def delete(self, request, *args, **kwargs):
        case_id = request.data.get(id)
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete("case_data_{}".format(case_id))

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            from django.core.cache import cache
            case = response.data
            cache.set("case_data_{}".format(case['id']), {
                'product': case['product'],
                'case_type': case['case_type']

            })
        return response


class BatchRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)
    get_queryset = BatchList.get_queryset
    lookup_field = 'id'
    serializer_class = BatchSerializer

    def delete(self, request, *args, **kwargs):
        batch_id = request.data.get(id)
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete("batch_data_{}".format(batch_id))

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            from django.core.cache import cache
            batch = response.data
            cache.set("batch_data_{}".format(batch['id']), {
                'cmd': batch['cmd'],
            })
        return response




class CustomBatchRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)
    get_queryset = CustomBatchList.get_queryset
    lookup_field = 'id'
    serializer_class = CustomBatchSerializer
    # queryset = CustomBatchList.get_queryset()

    def delete(self, request, *args, **kwargs):
        batch_id = request.data.get(id)
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete("batch_data_{}".format(batch_id))

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            from django.core.cache import cache
            batch = response.data
            cache.set("batch_data_{}".format(batch['id']), {
                'cmd_args': batch['cmd_args'],
            })
        return response
