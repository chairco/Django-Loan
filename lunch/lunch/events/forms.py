# events/forms.py
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Event, Order, Cocodri, Pegadri

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('store',)
        widgets = {'store': forms.HiddenInput}

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', submit_title))


class OrderForm(forms.ModelForm):
    
    cocodri = forms.ModelChoiceField(
        queryset=Cocodri.objects.all(),
        label='CoCo DRI'
      )
    pegadri = forms.ModelChoiceField(
        queryset=Pegadri.objects.all(),
        label='Pegadri DRI'
      )
    
    class Meta:
        model = Order
        fields = ('item', 'cocodri', 'pegadri', 'notes',)

    def __init__(self, *args, user=None, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].empty_label = None
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', submit_title))
        self.fields['cocodri'].queryset = Cocodri.objects.filter(owner=user)
        self.fields['pegadri'].queryset = Pegadri.objects.filter(owner=user)
