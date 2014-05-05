# -*- coding: utf-8 -*-
from django.contrib import admin
from cpan2repo.models import Package, ExcludePackage


class PackageAdmin(admin.ModelAdmin):
    pass


class ExcludePackageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Package, PackageAdmin)
admin.site.register(ExcludePackage, ExcludePackageAdmin)
