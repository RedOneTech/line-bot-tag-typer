from django.contrib import admin

from groups.models import LINEGroup, LINEGroupMember

admin.site.register([LINEGroup, LINEGroupMember])
