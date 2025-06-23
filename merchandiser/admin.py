from django.contrib import admin
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','company_phone')
    search_fields = ('name', 'email', 'company_phone')

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'department', 'wgr')
    search_fields = ('name', 'email', 'phone', 'department')
    list_filter = ('department',)


admin.site.register(Inquiry)
admin.site.register(Style)
admin.site.register(RepeatOf)
admin.site.register(Item)
admin.site.register(Fabrication)
admin.site.register(Color)
admin.site.register(ColorTotal)
admin.site.register(ColorSizeGroup)
admin.site.register(SizeQuantity)
admin.site.register(InquiryAttachment)
