from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        group = Group.objects.get(name='common')[0]
        user.groups.add(group)
        return user
