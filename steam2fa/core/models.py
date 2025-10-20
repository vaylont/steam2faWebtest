# steam2fa/core/models.py
from django.db import models
from .utils import decode_secret, totp_code, steam_guard_code


class SteamAccount(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    login = models.CharField(max_length=150, help_text="Логин Steam")
    shared_secret = models.CharField(max_length=200, blank=True, help_text="shared_secret (Base64/hex/Base32)")
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.login} ({self.shared_secret or 'no id'})"

    def get_steam_code(self, timestep: int = 30):
        if not self.shared_secret:
            raise ValueError("shared_secret не задан")
        key = decode_secret(self.shared_secret)  # Base64/hex/Base32 поддерживаются
        return steam_guard_code(key, timestep=timestep)
