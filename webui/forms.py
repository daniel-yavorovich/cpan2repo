from django.forms import forms, ModelForm
from webui.models import Branch, BuildConfiguration, PackageNameMapping


class BranchForm(ModelForm):

    class Meta:
        model = Branch
        fields = ['name', 'path', 'maintainer']


class BuildConfigurationForm(ModelForm):

    class Meta:
        model = BuildConfiguration
        fields = ['name', 'git_url', 'git_user', 'git_pass',
                  'git_branch', 'pkg_branch', 'install_root',
                   'pre_install_script', 'post_install_script',
                   'depends_list', 'auto_build']


class PackageNameMappingForm(ModelForm):

    class Meta:
        model = PackageNameMapping
        fields = ['orig_name', 'to_name']