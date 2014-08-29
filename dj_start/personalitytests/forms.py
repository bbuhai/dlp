from django import forms

from personalitytests.models import Test, Question


class PersTestForm(forms.Form):

    def __init__(self, test_id):
        super(PersTestForm, self).__init__()
        t = Test.objects.filter(test_id=test_id).all()


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.Textarea()
    sender = forms.EmailField()
    cc_self = forms.BooleanField(required=False)