from django.urls import path
from . import views
from .quotation import QuotationSession 
from django.shortcuts import redirect

app_name = 'quotation'

urlpatterns = [
    path('', views.view_quotation, name='view'),
    path('add/<int:item_id>/', views.add_to_quotation, name='add'),
    path('remove/<int:item_id>/', lambda r, item_id: QuotationSession(r).remove(item_id) or redirect('quotation:view'), name='remove'),
    path('submit/', views.submit_quotation, name='submit'),
    path('success/', views.success_view, name='success'),
    path('update/<int:item_id>/', views.update_quotation_quantity, name='update_quantity'),
]
