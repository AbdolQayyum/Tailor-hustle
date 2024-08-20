from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'picture',
            'first_name',
            'last_name',
            'username',
            'phone_number'
            )
        labels = {
            'phone_number': 'Phone'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'picture':
                self.fields[field].widget.attrs.update({'class': 'form-control-file'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm'})
