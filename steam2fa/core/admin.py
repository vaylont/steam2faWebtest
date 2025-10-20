from django.contrib import admin
from .models import SteamAccount

@admin.register(SteamAccount)
class SteamAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'created', 'short_secret', 'current_code')
    list_display_links = ('login',)
    search_fields = ('login',)
    readonly_fields = ('created',)




    def short_secret(self, obj):
        s = obj.shared_secret or ''
        return (s[:10] + '…') if len(s) > 10 else s
    short_secret.short_description = 'shared_secret'

    def current_code(self, obj):
        try:
            code, _ = obj.get_totp()
            return code
        except Exception:
            return '—'
    current_code.short_description = 'code'

