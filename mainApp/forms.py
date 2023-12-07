from django import forms
from django.contrib.auth import get_user_model


class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)


class EditUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'street', 'zip_code', 'city']
