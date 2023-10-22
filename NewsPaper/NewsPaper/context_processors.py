from django.contrib.auth.models import Group


def groups(request):
    groups = request.user.groups.all()
    groups = [group.name for group in groups]
    return {'groups':  groups}
