from django import forms
from .models import CustomUser


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Apna password daalo",
        }),
    )
    password2 = forms.CharField(
        label="Password Confirm Karo",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password dobara daalo",
        }),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "full_name")
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "aapka@gmail.com",
            }),
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Apna poora naam daalo",
            }),
        }
        labels = {
            "email": "Gmail Address",
            "full_name": "Poora Naam",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Sirf @gmail.com email address allowed hai.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Ye email pehle se registered hai. Login karo.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1", "")
        p2 = cleaned_data.get("password2", "")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Dono password same hone chahiye.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        plain = self.cleaned_data["password1"]
        user.set_password(plain)
        user.plain_password = plain
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Gmail Address",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "aapka@gmail.com",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password daalo",
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Sirf @gmail.com email se login kar sakte hain.")
        return email
