from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import MenuItem, Store


BaseMenuItemFormSet = inlineformset_factory(
    parent_model=Store, model=MenuItem, fields=('isn', 'store',), extra=1,
)


class MenuItemFormSet(BaseMenuItemFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = ('name', 'notes',)

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if submit_title:
            self.helper.add_input(Submit('submit', submit_title))

class ItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = (
            'isn', 'unit_no', 'config',
            'ffned', 'function_team',
            'store', 'utk', 'cg_color', 'hsg',
        )
        widgets = {
            'ffned': forms.Select(
                choices=[
                    #前面是值後面是顯示
                    ('0', 'FF'), 
                    ('1', 'NED')
                ]
            ),
        }

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if submit_title:
            self.helper.add_input(Submit('submit', submit_title))
