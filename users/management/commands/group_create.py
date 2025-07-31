from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        manager_group = Group.objects.create(name="managers")
        blocked_perm = Permission.objects.get(codename="can_blocked_user")
        view_perm = Permission.objects.get(codename="can_view_user")
        manager_group.permissions.add(blocked_perm, view_perm)
        manager_group.save()
