import re
import commands


def check_pkg_in_base_repo(deb_name):
    result = commands.getstatusoutput("apt-cache search %s" % deb_name)

    if result[0] == 0 and re.search("%s" % deb_name, result[1], re.I):
        return True
    else:
        return False