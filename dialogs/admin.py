from django.contrib import admin
from .models import Dialog, Query

admin.site.register([Dialog])


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = (
        "req",
        "dialog",
    )
