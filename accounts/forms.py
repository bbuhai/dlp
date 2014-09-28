from django.contrib.auth.forms import UserCreationForm
from django import forms


class NewUserForm(UserCreationForm):
    username = forms.RegexField(
        label="Username",
        max_length=30,
        regex=r'^[\w.]+$',
        help_text="Required. 30 characters or fewer. Letters, digits and "
                      "'.', '_' only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and "
                         "'.', '_' characters."})