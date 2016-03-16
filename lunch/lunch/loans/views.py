# loans/views.py
import logging
from datetime import datetime
from django.shortcuts import redirect, render
from .models import Loan, Device, Pegadri, Cocodri, Log
from django.http import Http404
#from django.forms.models import modelform_factory
from .forms import LoanForm, DeviceFormSet, AddpegadriForm, AddcocodriForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.forms.models import inlineformset_factory
from utility.pega_smtp import SMTP
from utility import HTML
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import JsonResponse

from .belta import Sfis

logger = logging.getLogger(__name__)

@login_required
def loan_list(request):
    loans = Loan.objects.all()
    Log.objects.create(name=request.user, function='loan list', info=None)
    return render(request, 'loans/loan_list.html', {'loans': loans})

@login_required
def loan_detail(request, pk):
    try:
        loan = Loan.objects.get(pk=pk)
    except Store.DoesNotExist:
        raise Http404
    Log.objects.create(name=request.user, function='loan detail', info=loan)
    return render(request, 'loans/loan_detail.html', {'loan': loan})

@login_required
def utk_search(request):
    if request.method == 'GET':
       #return render_to_response('loans/utk_search.html', locals())
       return render(request, 'loans/utk_search.html')

def utk_value(request):
    if request.method == 'POST':
        isn = request.POST.get('nickname','')
        #print('isn',isn)
        sfis = Sfis()
        s_utk = sfis.utk(isn)
        if s_utk[0] == 1:
            utk = {"UTK No Data":s_utk[1]}
        else:
            utk = s_utk[1]
        s_modd = sfis.modd(isn)
        if s_modd[0] == 1:
            modd = {"MODD No Data":s_modd[1]}
        else:
            modd = s_modd[1]
        print(type(utk), utk, type(modd), modd)
        Log.objects.create(name=request.user, function='utk search', info=str(isn)+str(utk)+str(modd))
        return JsonResponse(dict(utk, **modd))

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
                # send mail
                attach_mail = request.POST.getlist('pega_dri_mail_group')
                attach_mail = [Pegadri.objects.get(id=n).email for n in attach_mail]
                creater = User.objects.get(username=request.user).email
                #send_mail(request=loan, attach_mail=attach_mail, creater=creater)
                loan.save()
                device_formset.save()
                device_items = Device.objects.filter(request=loan)
                device_list = list()
                for i in range(0, len(device_items)):
                    # update sfis
                    try:
                        sfis = Sfis()
                    except Exception as e:
                        sfis = Sfis()

                    s_info = sfis.isninfo(device_items[i].isn)
                    s_utk = sfis.utk(device_items[i].isn)
                    s_error = sfis.error(device_items[i].isn, device_items[i].station)
                    s_modd = sfis.modd(device_items[i].isn)
                    if s_info[0] == 0:
                        info = s_info[1]
                        config = info['SN1'].split('/')[3]
                        unit_no = info['SN1'].split('/')[4]
                        Device.objects.filter(isn=device_items[i].isn).update(
                            config=config, unit_no=unit_no, sfis_status=True
                        )
                    else:
                        info = s_info[1]
                        Device.objects.filter(isn=device_items[i].isn).update(
                            sfis_info=str(info)+','+str(datetime.strftime(datetime.now(),'%Y-%m-%d-%H:%M'))
                        )
                    if s_utk[0] == 0:
                        utk = s_utk[1]
                        Device.objects.filter(isn=device_items[i].isn).update(
                            utk=utk['C_TIME']
                        )
                    if s_error[0] == 0:
                        serror = s_error[1]
                        failure_symptoms = serror['PDCS_LIST_OF_FAILTING_TEST']
                        Device.objects.filter(isn=device_items[i].isn).update(
                            failure_symptoms=failure_symptoms 
                        )
                    else:
                        serror = s_error[1]
                        failure_symptoms = str(serror)
                        Device.objects.filter(isn=device_items[i].isn).update(
                            failure_symptoms=str(serror)
                        )
                    if s_modd[0] == 0:
                       smodd = s_modd[1]
                       grpnm = str(smodd['GRPNM'])+', '+str(smodd['STATUS'])
                       Device.objects.filter(isn=device_items[i].isn).update(
                            grpnm=str(grpnm)
                        )
                    else:
                       smodd = s_modd[1]
                       grpnm = str(smodd)
                       Device.objects.filter(isn=device_items[i].isn).update(
                            grpnm=str(grpnm)
                        )
                    device_list.append(
                        [str(device_items[i].isn), str(device_items[i].station),
                         str(grpnm), str(config), str(unit_no),
                         str(failure_symptoms)]
                    )
                send_mail(request=loan, device=device_list, attach_mail=attach_mail, creater=creater)
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
@permission_required('loans.delete_store', login_url='/accounts/login/')
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

def send_mail(request, device, attach_mail, creater):
    # pega dri and coco dir should be unie.
    pega_dri_email = request.pegadri.email
    coco_dri_email = request.cocodri.email
    mail_group = [
        pega_dri_email, coco_dri_email, creater,
        'Gina2_Huang@pegatroncorp.com',
        'Rebecca_Chang@pegatroncorp.com',
        'Adrian_Wang@pegatroncorp.com',
        'Yichieh_chen@pegatroncorp.com'
    ]
    # testing: 
    mail_group = mail_group + attach_mail
    # html header hot code
    header = [
                '#',
                'function_team',
                'cocodri', 
                'pegadri', 
                'purpose',
                'disassemble',
                'created_at',
                'creater'
    ]
    device_header = [
            'ISN',
            'Station',
            'GRPNM',
            'Config',
            'Unit_NO.',
            'Failure Symptoms'
    ]

    # make html content
    typestyle = ['font-family:Calibri;font-size: 13px']*(len(header)+1)
    html_title = list()
    # check disassemble or not
    assembly = ""
    if request.disassemble == True:
        assembly = "YES"
    elif request.disassemble == False:
        assembly = "No"
    # 轉全形為半形(要透過forms去卡掉)
    #request.request_condition = strQ2B(request.request_condition)
    request.pegadri.name = strQ2B(request.pegadri.name)
    request.purpose = strQ2B(request.purpose)
    data = [[
        #str(request.request_condition).replace('、',';'), 
        str(request.id),
        str(request.function_team),
        str(request.cocodri.name), 
        str(request.pegadri.name),
        str(request.purpose), 
        str(assembly),
        str(datetime.strftime(datetime.now(),'%Y-%m-%d-%H:%M')),
        str(creater)
    ]]
    
    # loan html
    for row in header:
        html_title.append(HTML.TableCell(row, bgcolor='silver', 
                        style='font-family:Calibri;font-size: 15px'))
    htmlcode = HTML.table(data, header_row=html_title, col_styles=typestyle)
    # device html
    dhtml_title = list()
    ddata = device
    for row in device_header:
        dhtml_title.append(HTML.TableCell(row, bgcolor='silver',
                        style='font-family:Calibri;font-size: 15px'))
    dhtmlcode = HTML.table(ddata, header_row=dhtml_title, col_styles=typestyle)
    htmlcode = htmlcode + dhtmlcode + \
        '<p><a href=http://172.28.146.16:8082/loan/'+str(request.id)+'/>清單連結</a></p>'

    try:
        #mail = Mailcontent.objects.get(id=1)
        #mail.content = str(mail.content).replace('\r\n', '<br>')
        mail_content = "Hi,"
        mail_content = """\
        <html>
          <head></head>
          <body>
            <p><font face='Calibri'>
            %s
            </p>
          </body>
        </html>
        """ % mail_content

        smtp = SMTP()
        smtp.send(recipients=mail_group, title="Kirin TDL-"+str(request.purpose), 
                text_source=mail_content+htmlcode)
    except Exception as e:
        raise e

def strQ2B(ustring):
    """把字元串全形轉半形"""
    rstring = ""
    for uchar in ustring:
        #print uchar, ord(uchar)
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        elif inside_code <= 0xFF5E and inside_code >= 0xFF01:
            inside_code -= 0xfee0
        elif inside_code == 12289:
            inside_code = 0x0020
        else:
            pass
            #rstring += uchar
            #print uchar, ord(uchar)
        ##else:
        ##    inside_code -= 0xfee0
        #if inside_code < 0x0020 or inside_code > 0x7e:   #轉完之後不是半形字元返回原來的字元
        #    rstring += uchar
        rstring += chr(inside_code)
    return rstring

@login_required
def export_xlsx(request):
    from .excel_utility import WriteToExcel
    request_list = Loan.objects.all().order_by('function_team')
    '''
    for i in xrange(0, len(request_list)):
        print request_list[i].request_condition, request_list[i].quantity
    '''
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=CheckinFA_Report_'+ \
                                      datetime.strftime(datetime.now(), '%Y%m%d%H%M') +'.xlsx'
    xlsx_data = WriteToExcel(request_data=request_list)
    response.write(xlsx_data)
    Log.objects.create(name=request.user, function='Download report', info=None)
    return response
