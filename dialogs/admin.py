from django.contrib import admin
from .models import Dialog, Query

admin.site.register([Dialog, Query])