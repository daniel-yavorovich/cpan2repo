from django import forms
from webui.models import Branch, BuildConfiguration, PackageNameMapping


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'path', 'maintainer', 'is_virtual']


CONF_TYPE = (
    ("deb", "Debian package"),
    ("remote", "Remote script"),
)


class BaseForm(forms.ModelForm):
    conf_type = forms.ChoiceField(choices=CONF_TYPE)


class BuildConfigurationForm(BaseForm):

    pkg_branch = forms.ModelChoiceField(queryset=Branch.objects.exclude(pk=1))

    def __init__(self, *args, **kwargs):
        super(BuildConfigurationForm, self).__init__(*args, **kwargs)
        for key in ['pkg_branch', 'install_root']:
            self.fields[key].required = True

    class Meta:
        model = BuildConfiguration
        fields = ['conf_type', 'name', 'git_url', 'git_user', 'git_pass',
                  'git_branch', 'git_subdir', 'pkg_branch', 'install_root',
                  'build_script', 'pre_install_script',
                  'post_install_script', 'depends_list',
                  'build_on_commit_in', 'auto_build']


class RemoteBuildConfigurationForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super(RemoteBuildConfigurationForm, self).__init__(*args, **kwargs)
        for key in ['remote_ip', 'ssh_user', 'ssh_pass', 'build_script']:
            self.fields[key].required = True

    class Meta:
        model = BuildConfiguration
        fields = ['conf_type', 'name', 'git_url', 'git_user', 'git_pass',
                  'git_branch', 'build_script',
                  'remote_ip', 'ssh_port',
                  'ssh_user', 'ssh_pass',
                  'build_on_commit_in', 'auto_build']


class PackageNameMappingForm(forms.ModelForm):

    class Meta:
        model = PackageNameMapping
        fields = ['orig_name', 'to_name']