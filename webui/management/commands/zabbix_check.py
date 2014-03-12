from django.core.management.base import BaseCommand, CommandError
from webui.models import BuildConfiguration, Branch


def check_errors_build_confs():
    error_build_confs = BuildConfiguration.objects.filter(status=4)

    if not error_build_confs:
        return "OK"
    elif len(error_build_confs) == 1:
        return "%s %s" % (error_build_confs[0].name, error_build_confs[0].pkg_branch.name)
    else:
        errors_list_by_branch = []
        for branch in Branch.objects.all():
            branch_errors_build_confs = branch.buildconfiguration_set.filter(status=4)
            if not branch_errors_build_confs:
                continue
            errors_list_by_branch.append("%d packages in %s" % (branch_errors_build_confs.count(), branch.name))
        return ", ".join(errors_list_by_branch)


class Command(BaseCommand):
    help = 'Check build errors'

    def handle(self, *args, **options):
        self.stdout.write(check_errors_build_confs() + "\n")