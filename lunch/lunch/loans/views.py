# loans/views.py
import logging

from django.shortcuts import redirect, render
from .models import Loan, Device, Pegadri, Cocodri
from django.http import Http404
#from django.forms.models import modelform_factory
from .forms import LoanForm, DeviceFormSet, AddpegadriForm, AddcocodriForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms.models import inlineformset_factory

logger = logging.getLogger(__name__)

def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'loans/loan_list.html', {'loans': loans})

def loan_detail(request, pk):
    try:
        loan = Loan.objects.get(pk=pk)
    except Store.DoesNotExist:
        raise Http404
    return render(request, 'loans/loan_detail.html', {'loan': loan})

@login_required
def loan_create(request):
    if request.method == 'POST':
        formp = AddpegadriForm()
        formc = AddcocodriForm()
        form = LoanForm(request.POST, submit_title='建立', user=request.user)
        if form.is_valid():
            loan = form.save(commit=False)
            if request.user.is_authenticated():
                loan.owner = request.user
            device_formset = DeviceFormSet(request.POST, instance=loan)
            if device_formset.is_valid():
                loan.save()
                device_formset.save()
                return redirect(loan.get_absolute_url())
        # TODO(yichieh): if form is fail, should also return device_formset value by user input.
        return render(request, 'loans/loan_create.html', {
            'form': form, 'formp': formp, 'formc': formc,
        })
    else:
        formp = AddpegadriForm()
        formc = AddcocodriForm()
        form = LoanForm(submit_title=None, user=request.user)
        form.helper.form_tag = False
        device_formset = DeviceFormSet()
    return render(request, 'loans/loan_create.html', {
        'form': form, 'formp': formp, 'formc': formc,
        'device_formset': device_formset,
    })

@login_required
def loan_update(request, pk):
    try:
        loan = Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan, submit_title='更新', user=request.user)
        # 用 post data 建立 formset，並在其（與 loan form）合法時儲存。
        device_formset = DeviceFormSet(request.POST, instance=loan)
        if form.is_valid() and device_formset.is_valid():
            loan = form.save()
            device_formset.save()
            return redirect(loan.get_absolute_url())
    else:
        # 移除 submit button 與 form tag。
        form = LoanForm(instance=loan, submit_title=None, user=request.user)
        form.helper.form_tag = False
        device_formset = DeviceFormSet(instance=loan)

    return render(request, 'loans/loan_update.html', {
        'form': form, 'loan': loan, 'device_formset': device_formset,
    })

@login_required
@require_http_methods(['POST', 'DELETE'])
def loan_delete(request, pk):
    try:
        loan = Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        raise Http404
    '''
    if (not loan.owner or loan.owner == request.user
            or request.user.has_perm('loan_delete')):
        loan.delete()
        return redirect('loan_list')
    '''
    if loan.can_user_delete(request.user):
        loan.delete()
        if request.is_ajax():
            return HttpResponse()
        return redirect('loan_list')
    return HttpResponseForbidden()

def adddri_pega(request):
    if request.method == 'POST':
        formp = AddpegadriForm(request.POST)
        if formp.is_valid():
            post = formp.save(commit=False)
            post.author = request.user
            post.owner = request.user
            post.save()
            # get the user id from db
            select_id = Pegadri.objects.filter(name=post.name)
            select_id = select_id[len(select_id)-1].id
            return HttpResponse(select_id)
    return HttpResponse("False")

def adddri_coco(request):
    if request.method == 'POST':
        formc = AddcocodriForm(request.POST)
        if formc.is_valid():
            post = formc.save(commit=False)
            post.author = request.user
            post.owner = request.user
            post.save()
            # get the user id from db
            select_id = Cocodri.objects.filter(name=post.name)
            select_id = select_id[len(select_id)-1].id
            return HttpResponse(select_id)
    return HttpResponse("False")