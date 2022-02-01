from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['username'].help_text = None
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'special_user', 'is_author')
