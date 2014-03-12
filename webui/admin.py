from django.contrib import admin
from webui.models import Branch, BuildConfiguration, PackageNameMapping


class BranchAdmin(admin.ModelAdmin):
    pass


class BuildConfigurationAdmin(admin.ModelAdmin):
    pass


class PackageNameMappingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Branch, BranchAdmin)
admin.site.register(BuildConfiguration, BuildConfigurationAdmin)
admin.site.register(PackageNameMapping, PackageNameMappingAdmin)
