from item.models import Item

class QuotationSession:
    def __init__(self, request):
        self.session = request.session
        quotation = self.session.get('quotation')
        if not quotation:
            quotation = self.session['quotation'] = {}
        self.quotation = quotation

    def add(self, item_id, quantity):
       item_id = str(item_id)
       if item_id in self.quotation:
           self.quotation[item_id] += quantity
       else:
           self.quotation[item_id] = {'quantity': quantity}
       self.save()

    def remove(self, item_id):
        item_id = str(item_id)
        if item_id in self.quotation:
            del self.quotation[item_id]
            self.save()

    def update(self, item_id, quantity):
        item_id = str(item_id)
        if item_id in self.quotation:
            self.quotation[item_id]['quantity'] = quantity
        else:
            self.quotation[item_id] = {'quantity': quantity}
        self.save()

    def clear(self):
        self.session['quotation'] = {}
        self.session.modified = True

    def update_quantity(self, item_id, quantity): 
        item_id = str(item_id)
        if item_id in self.quotation:
            self.quotation[item_id]['quantity'] = quantity
            self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        item_ids = self.quotation.keys()
        items = Item.objects.filter(id__in=item_ids)
        return [
            {
                'item': item,
                'quantity': self.quotation[str(item.id)]['quantity']
            }
            for item in items
        ]
