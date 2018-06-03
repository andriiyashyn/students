from django.contrib import admin

from core.models_dir.user_model import Client


class ClientAdmin(admin.ModelAdmin):
    model = Client


admin.site.register(Client, ClientAdmin)
