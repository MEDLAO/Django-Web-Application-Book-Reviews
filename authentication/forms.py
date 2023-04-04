from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur',
                               widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe"}),
                               label='Mot de passe')
    # the widget determines how to display the field, here the password is hidden


class SignupForm(UserCreationForm):  # UserCreationForm is a ModelForm
    class Meta(UserCreationForm.Meta):  # as we inherit from a ModelForm
        model = get_user_model()        # we also inherit from the Meta class if we need to supercharge it
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = "Nom d'utilisateur"
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmation mot de passe'
