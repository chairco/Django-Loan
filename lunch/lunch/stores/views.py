# store/view.py
import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from events.forms import EventForm
from .forms import MenuItemFormSet, StoreForm, ItemForm
from .models import Store, MenuItem

from django.shortcuts import render, get_object_or_404

logger = logging.getLogger(__name__)


def store_list(request):
    stores = Store.objects.all()
    return render(request, 'stores/store_list.html', {'stores': stores})

def store_detail(request, pk):
    try:
        store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        raise Http404
    event_form = EventForm(initial={'store': store}, submit_title='建立活動')
    event_form.helper.form_action = reverse('event_create')
    return render(request, 'stores/store_detail.html', {
        'store': store, 'event_form': event_form,
    })

def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, submit_title='建立')
        if form.is_valid():
            store = form.save(commit=False)
            if request.user.is_authenticated():
                store.owner = request.user
            store.save()
            logger.info('New store {store} created by {user}!'.format(
                store=store, user=request.user
            ))
            return redirect(store.get_absolute_url())
    else:
        form = StoreForm(submit_title='建立')
    return render(request, 'stores/store_create.html', {'form': form})

def store_update(request, pk):
    try:
        store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store, submit_title='更新')
        menu_item_formset = MenuItemFormSet(request.POST, instance=store)
        if form.is_valid() and menu_item_formset.is_valid():
            store = form.save()
            menu_item_formset.save()
            return redirect(store.get_absolute_url())
    else:
        form = StoreForm(instance=store, submit_title=None)
        form.helper.form_tag = False
        menu_item_formset = MenuItemFormSet(instance=store)

    return render(request, 'stores/store_update.html', {
        'form': form, 'store': store, 'menu_item_formset': menu_item_formset,
    })

def item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
            #return redirect(item.get_absolute_url())
            return redirect('stores.views.store_detail', pk=item.store_id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'stores/item_detail.html', {'form': form})

@login_required
@require_http_methods(['POST', 'DELETE'])
def store_delete(request, pk):
    try:
        store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        raise Http404
    if store.can_user_delete(request.user):
        store.delete()
        if request.is_ajax():
            return HttpResponse()
        return redirect('store_list')
    return HttpResponseForbidden()
