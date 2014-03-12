import re
import commands
from django.conf import settings
from metacpan import get_release_info


def get_pkg_depends(cpan_name):
    cpan_name = cpan_name.replace("-", "::")
    depends = []

    result = commands.getstatusoutput("%s -q --showdeps %s" % (settings.CPANM_PATH, cpan_name))

    for line in result[1].split("\n"):
        if '!' in line or " " in line:
            continue

        orig_module_name = re.split("(x*)\~", line)[0]

        # exclude dependence set for standard modules
        if check_standard_module(orig_module_name):
            continue

        module_name = get_release_info(orig_module_name)["metadata"]["name"]

        if re.search('^perl$', module_name, re.I) or re.search('^lib.*-perl$', module_name, re.I) or re.search('^PerlMagick$', orig_module_name, re.I):
            deb_name = module_name.lower()
        else:
            deb_name = "lib{cpan_name}-perl".format(
                cpan_name=module_name,
            ).replace("::", "-").replace("_", "").lower()

        if module_name and deb_name:
            depends.append({
                "orig_module_name": orig_module_name,
                "module_name": module_name,
                "deb_name": deb_name
            })

    return depends


def check_standard_module(cpan_name):
    cpan_name = cpan_name.replace("-", "::")
    result = commands.getstatusoutput("%s %s" % (settings.CHECK_CORE_MODULE_PATH, cpan_name))

    if result[0] == 0:
        return False
    else:
        return True