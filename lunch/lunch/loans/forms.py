# loans/forms.py
from django import forms
from .models import Loan
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.models import inlineformset_factory

from .models import Device, Cocodri, Pegadri, Functionteam

BaseMenuItemFormSet = inlineformset_factory(
    parent_model=Loan, model=Device, fk_name='request', fields=('isn', 'station',),
    extra=1,
)

class DeviceFormSet(BaseMenuItemFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False        # 我們要自己包。
        self.helper.disable_csrf = True     # DeviceForm 已經有 CSRF token，不需要重複產生。

class AddpegadriForm(forms.ModelForm):
    
    class Meta:
        model = Pegadri
        fields = (
                  'name', 'email'
          )
        labels = {
                  'name': 'PEGA DRI NAME',
                  'email':  'PEGA DRI EMAIL'
        }
        # 設定協助描述的文字
        help_texts = {
          'name': '@請勿輸入全型字型例如:錯誤:％, 正確:%.',
          'email': '@請勿輸入全型字型例如:錯誤:％, 正確:%.'
        }

class AddcocodriForm(forms.ModelForm):
    
    class Meta:
        model = Cocodri
        fields = (
                  'name', 'email'
          )
        labels = {
                  'name': 'COCO DRI NAME',
                  'email':  'COCO DRI EMAIL'
        }
        # 設定協助描述的文字
        help_texts = {
          'name': '@請勿輸入全型字型例如:錯誤:％, 正確:%.',
          'email': '@請勿輸入全型字型例如:錯誤:％, 正確:%.'
        }

class LoanForm(forms.ModelForm):

    cocodri = forms.ModelChoiceField(
        queryset=Cocodri.objects.all().order_by('name'),
        label='CoCo DRI',
        help_text='@DRI不在選單內請先新增. \
           <button type="button" class="btn btn-info btn-xs" data-style="zoom-in" \
           data-toggle="modal" data-target="#cocoModal" \
           data-whatever="@pega"> <span class="ladda-label">新增CoCo DRI</span></button>'
      )
    pegadri = forms.ModelChoiceField(
        queryset=Pegadri.objects.exclude(name__istartswith='%').order_by('name'),
        label='Pega DRI',
        help_text='@DRI不在選單內請先新增. 注意,群組信箱不會顯示. \
           <button type="button" class="btn btn-info btn-xs" data-style="zoom-in" \
           data-toggle="modal" data-target="#pegaModal" \
           data-whatever="@pega"> <span class="ladda-label">新增PEGA DRI</span></button>'
      )
    pega_dri_mail_group = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Pegadri.objects.all().order_by('name'),
        label='PEGA DRI Mail Group',
        #'@加入更多member (MAC OS)請使用command+左鍵/(Win OS)請使用CTRL+左鍵 選擇多個.
        help_text='@加入更多member，點選滑鼠一下左邊方格內人名 加至 右邊方格就算成功.<br> \
        @DRI不在選單內請先新增. \
        <button type="button" class="btn btn-info btn-xs" data-style="zoom-in" \
        data-toggle="modal" data-target="#pegaModal" \
        data-whatever="@pega"> <span class="ladda-label">新增PEGA DRI</span></button>',
        widget=forms.SelectMultiple(attrs={'size':'10'})
      )
    function_team = forms.ModelChoiceField(
       queryset=Functionteam.objects.all().order_by('name'),
       label='Function Team'
    )
    #disassemble = forms.MultipleChoiceField(required=True,
    #    widget=forms.CheckboxSelectMultiple, choices=[('False', 'False'), ('True', 'True')])   
    disassemble = forms.ChoiceField(
        required=True, 
        widget=forms.RadioSelect, 
        choices=[('False', 'No',), ('True', 'Yes',)],
        label='Will unit be opened'
    )

    class Meta:
        model = Loan
        fields=(
            'function_team', 'cocodri', 'pegadri', 'purpose', 'disassemble',
            'pega_dri_mail_group',
        )
        labels = {
            'disassemble': 'Will unit be opened',
        }
 
    def __init__(self, *args, user=None, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if submit_title:
            self.helper.add_input(Submit('submit', submit_title))
        self.fields['cocodri'].queryset = Cocodri.objects.filter(owner=user)
        self.fields['pegadri'].queryset = Pegadri.objects.filter(owner=user)
        self.fields['pega_dri_mail_group'].queryset = Pegadri.objects.filter(owner=user)
