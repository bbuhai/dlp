from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, min_length=2)
    message = forms.CharField(min_length=5, widget=forms.Textarea)
    sender = forms.EmailField(required=True)
    cc_self = forms.BooleanField(required=False)

    def is_valid(self, *args, **kwargs):
        # if len(self.data['message']) < 5:
        #     pass
        super(ContactForm, self).is_valid()

    def clean(self, *args, **kwargs):
        return super(ContactForm, self).clean(*args, **kwargs)