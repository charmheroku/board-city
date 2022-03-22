from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin


class BannedUsersGroup(UserPassesTestMixin):
    """Миксин для блокирования забанненых юзеров"""
    def test_func(self):
        return not self.request.user.groups.filter(name="banned_users").exists()

    def handle_no_permission(self):
        messages.error(self.request, "Вы не можете добавить объявление")
        return redirect(reverse("main:user_edit"))
