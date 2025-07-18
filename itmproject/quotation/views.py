from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .quotation import QuotationSession
from .models import Quotation, QuotationItem
from item.models import Item
from django.contrib import messages

@login_required
def add_to_quotation(request, item_id):
    quotation = QuotationSession(request)
    quotation.add(item_id=item_id, quantity=1)
    return redirect('quotation:view')

@login_required
def view_quotation(request):
    quotation = QuotationSession(request)
    items = quotation.get_items()
    return render(request, 'quotation/view_quotation.html', {'items': items})

@login_required
def submit_quotation(request):
    quotation = QuotationSession(request)
    
    if request.method == 'POST':
        
        for entry in quotation.get_items():
            item_id = str(entry['item'].id)
            form_quantity = request.POST.get(f'qty_{item_id}')
            if form_quantity:
                try:
                    quantity = int(form_quantity)
                    quotation.update_quantity(item_id, quantity)
                except ValueError:
                    continue

        if not quotation.get_items():
            messages.error(request, "Please add at least one item before submitting your quotation.")
            return redirect('quotation:view')
        
        q = Quotation.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address=request.POST['address']
        )

        for entry in quotation.get_items():
            QuotationItem.objects.create(
                quotation=q,
                item=entry['item'],
                quantity=entry['quantity']
            )
        quotation.clear()
        return redirect('quotation:success')
    else:
        items = quotation.get_items()
        return render(request, 'quotation/view_quotation.html', {'items': items})

@login_required
def success_view(request):
    return render(request, 'quotation/success.html')

@login_required
def update_quotation_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        quotation = QuotationSession(request)
        quotation.update_quantity(item_id, quantity)
    return redirect('quotation:view')