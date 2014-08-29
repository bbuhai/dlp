from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.Textarea()
    sender = forms.EmailField()
    cc_self = forms.BooleanField(required=False)