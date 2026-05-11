from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import SignupClosedException
from django.contrib.auth import get_user_model

User = get_user_model()


class GmailOnlySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email", "")
        if not email.lower().endswith("@gmail.com"):
            raise SignupClosedException("Sirf @gmail.com accounts allowed hain.")

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        email = data.get("email", "")
        user.email = email.lower()
        name = data.get("name", "")
        if name:
            user.full_name = name
        return user
