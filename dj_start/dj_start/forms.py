from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.Textarea(attrs={'required': True})
    sender = forms.EmailField(required=True)
    cc_self = forms.BooleanField(required=False)

    def is_valid(self, *args, **kwargs):
        if len(self.data['message']) < 5:
            pass
        super(ContactForm, self).is_valid()
