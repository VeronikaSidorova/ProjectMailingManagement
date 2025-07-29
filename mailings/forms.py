from django import forms
from django.forms import BooleanField

from mailings.models import Campaign, Recipient, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class CampaignForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ["start_time", "message", "recipients"]
        widgets = {
            'recipients': forms.SelectMultiple(),  # или forms.SelectMultiple()
            'message': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # ожидаем user при инициализации формы
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['recipients'].queryset = Recipient.objects.filter(owner=user)
            self.fields['message'].queryset = Message.objects.filter(owner=user)
