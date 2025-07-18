from django.contrib import admin

from .models import Quotation, QuotationItem

class QuotationItemInline(admin.TabularInline): 
    model = QuotationItem
    extra = 0

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'submitted_at')
    inlines = [QuotationItemInline]

@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'item', 'quantity')

