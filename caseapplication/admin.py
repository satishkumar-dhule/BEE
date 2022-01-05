from django.contrib import admin
from .models import Case, Product, Target, CustomBatch


@admin.register(Case)
class caseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'period', 'case_type', 'status', 'update_user_id', 'update_datetime', 'add_user_id', 'add_datetime')
    list_editable = ('product', 'period', 'case_type', 'status', 'update_user_id')
    list_display_links = ('id',)


@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    # list_display =Target.__class__.get
    pass

@admin.register(CustomBatch)
class CustomBatchAdmin(admin.ModelAdmin):
    # list_display =Target.__class__.get
    list_display = ('id',)