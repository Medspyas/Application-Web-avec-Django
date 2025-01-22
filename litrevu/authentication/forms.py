from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms


class SignupForm(UserCreationForm):
    # Personalisation du formaulaire d'inscription.
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

        self.fields["username"].label = "Identifiant"
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = "Confirmation Mot de passe"

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )
            field.label = ""

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2


class CustomAuthenticationForm(AuthenticationForm):
    # Personnalisation du formulaire d'authentification.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Nom d'utilisateur",
                "class": "form-control",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Mot de passe",
                "class": "form-control",
            }
        )
        self.error_messages["invalid_login"] = "Identifiant ou mot de passe incorrect"
