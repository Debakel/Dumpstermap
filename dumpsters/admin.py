from django.contrib import admin

from .models import Dumpster, Voting


class VotingAdmin(admin.ModelAdmin):
    list_display = ('dumpster', 'created_date', 'name', 'value', 'comment')
admin.site.register(Voting, VotingAdmin)


class DumpsterAdmin(admin.ModelAdmin):
    list_display = ('created', 'rating')
admin.site.register(Dumpster, DumpsterAdmin)
