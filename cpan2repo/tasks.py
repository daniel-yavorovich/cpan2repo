from __future__ import absolute_import
import os
import re
import shutil
import logging
import commands
import datetime
import paramiko
from celery import shared_task
from django.conf import settings
from cpan2repo.cpanm import get_pkg_depends
from cpan2repo.metacpan import get_release_info
from cpan2repo.models import Package, ExcludePackage
from webui.models import BuildConfiguration, PackageNameMapping
from cpan2repo.cpanm import check_standard_module


def get_git_url(url_base, user, password):
    git_url_schema, git_url_host_and_path = re.search("(htt.*:\/\/)(.*)", url_base).groups()
    return "{git_url_schema}{git_user}:{git_pass}@{git_url_host_and_path}".format(
        git_url_schema=git_url_schema,
        git_user=user,
        git_pass=password,
        git_url_host_and_path=git_url_host_and_path
    )


def stop_by_error(build_conf, error_log):
    build_conf.status = 4
    build_conf.auto_build = False
    build_conf.build_log = str(error_log)
    build_conf.save()


def get_ref_id(build_conf):
    git_url = get_git_url(build_conf.git_url, build_conf.git_user, build_conf.git_pass)
    ref_id = None

    try:
        command = "git ls-remote {git_url} refs/heads/{branch}".format(git_url=git_url, branch=build_conf.git_branch)
        ref_id = unicode(commands.getstatusoutput(command)[1].split("\t")[0])
    except:
        pass

    # GIT commit id require one word, does not have any " " in content.
    if " " in ref_id:
        ref_id = None

    return ref_id


@shared_task
def make_deb_from_cpan(cpan_name, pass_ignore=False):
    """
    Build deb from cpan
    """

    release_info = get_release_info(cpan_name)

    if not release_info:
        logging.error("Module %s does not have release info" % cpan_name)
        return False

    module_name = release_info["metadata"]["name"]

    # Generate debian module name
    if PackageNameMapping.objects.filter(orig_name=module_name):
        package_name = PackageNameMapping.objects.get(orig_name=module_name).to_name
    else:
        package_name = "lib{cpan_name}-perl".format(
            cpan_name=module_name,
        ).replace("::", "-").replace("_", "").lower()

    # Exit, if package excluded
    if ExcludePackage.objects.filter(name=package_name) and not pass_ignore:
        logging.warn("Package %s is excluded" % package_name)
        return False

    # Exit, if package already exist
    if Package.objects.filter(name=package_name) and not pass_ignore:
        logging.warn("Package %s already exist in internal repo" % package_name)
        return False

    # Adding package into local DB
    pkg = Package.objects.create(name=package_name)

    logging.warn("Building package \"%s\" ..." % package_name)

    # Get dependence list (only production runtime packages)
    package_dependence = get_pkg_depends(cpan_name)

    deb_depends = []

    # Send task for build dependence modules
    for mod_name in package_dependence:
        if ExcludePackage.objects.filter(name=mod_name["deb_name"]):
            continue

        deb_depends.append(mod_name["deb_name"])
        print "Depend for %s: %s" % (cpan_name, mod_name["deb_name"])

        if not Package.objects.filter(name=mod_name["deb_name"]):
            make_deb_from_cpan.delay(mod_name["orig_module_name"])

    # Change package statuses in DB
    pkg.status = 2
    pkg.save()

    # Formulation build command
    build_command = "dh-make-perl --cpan %s --build --recursive --core-ok --pkg-perl --arch all" % cpan_name
    if deb_depends:
        build_command += " --depends %s" % ",".join(deb_depends)

    # Inside into temp build directory and start deb build from cpan
    os.chdir(settings.TMP_BUILD_DIR)
    os.environ["DEB_BUILD_OPTIONS"] = "nocheck"
    build_result = commands.getstatusoutput(build_command)

    if "--- Done" in build_result[1]:
        pkg.status = 3
        pkg.save()
        logging.warn("Package %s build successful" % cpan_name)
        return True
    else:
        pkg.delete()
        logging.error("Package %s does not build" % cpan_name)
        return False


def build_pkg(build_conf_id):
    """
    Build debian package from
    application git repo,
    make tasks for build depends
    packages
    """

    build_conf = BuildConfiguration.objects.get(pk=build_conf_id)

    build_conf.status = 2
    build_conf.version += 1
    build_conf.save()

    PKG_BUILD_DIR = "%s_%s_%s" % (build_conf.name, build_conf.pk, build_conf.version)
    PACKAGE_NAME = "%s_%s" % (build_conf.name, build_conf.version)

    os.chdir(settings.TMP_BUILD_DIR)

    git_url = get_git_url(build_conf.git_url, build_conf.git_user, build_conf.git_pass)

    last_commit_id = get_ref_id(build_conf)

    if not last_commit_id:
        stop_by_error(build_conf, "Can't get last commit ID. Please check GIT url, login info / branch name.")
        return False

    # Checkout git repo
    git_clone_res = commands.getstatusoutput(
        "git clone -b {git_branch} {git_url} {pkg_build_dir}".format(
            git_branch=build_conf.git_branch,
            git_url=git_url,
            pkg_build_dir=PKG_BUILD_DIR)
    )

    if git_clone_res[0]:
        stop_by_error(build_conf, git_clone_res[1])
        return False

    try:
        os.chdir(PKG_BUILD_DIR)
    except Exception as e:
        stop_by_error(build_conf, e)
        return False

    if build_conf.build_script:
        buildscriptfile_path = "/tmp/buildscript_%d-%d.sh" % (build_conf.pk, build_conf.version)
        buildscriptfile = open(buildscriptfile_path, "w")
        buildscriptfile.write(str(build_conf.build_script.replace("\r", "")))
        buildscriptfile.close()
        os.chmod(buildscriptfile_path, 0775)
        buildscript_result = commands.getstatusoutput(buildscriptfile_path)
        os.unlink(buildscriptfile_path)
        if buildscript_result[0]:
            stop_by_error(build_conf, buildscript_result[1])
            return False

    build_conf.last_commit_id = last_commit_id
    build_conf.save()

    # Create package dirs
    os.mkdir(PACKAGE_NAME)
    os.mkdir("%s/DEBIAN" % PACKAGE_NAME)

    # Create install root in package
    root_dir = ("%s/%s" % (PACKAGE_NAME, build_conf.install_root))
    try:
        os.makedirs(root_dir)
    except OSError:
        pass

    # Get depends list
    depends_list = [line for line in build_conf.depends_list.replace("\r", "").split('\n') if line.strip() != '']

    if "cpanfile" in os.listdir("."):
        for line in open("cpanfile", "r").readlines():
            try:
                module_name = get_release_info(line.split("'")[1])["metadata"]["name"]
            except:
                continue

            if PackageNameMapping.objects.filter(orig_name=module_name):
                pkg_name = PackageNameMapping.objects.get(orig_name=module_name).to_name
            else:
                pkg_name = "lib{cpan_name}-perl".format(
                    cpan_name=module_name,
                ).replace("::", "-").replace("_", "").lower()

            if check_standard_module(module_name):
                continue

            depends_list.append(pkg_name)

            if ExcludePackage.objects.filter(name=pkg_name):
                continue

            if not Package.objects.filter(name=pkg_name):
                make_deb_from_cpan.delay(module_name)

    # Complectation deb package
    for dirname in os.listdir("."):
        if PACKAGE_NAME in dirname or ".git" in dirname:
            continue
        os.rename(dirname, "{dist_path}/{dir_name}".format(
            dist_path=root_dir,
            dir_name=dirname
        ))

    # Create package config files
    controlfile = open("%s/DEBIAN/control" % PACKAGE_NAME, "w")
    controlfile_content = """Package: {package_name}
Version: {package_version}
Architecture: all
Maintainer: {maintainer}
Section: perl
Priority: optional
Homepage: https://github.com/daniel-yavorovich/cpan2repo.git
Description: {description}
""".format(
        package_name=build_conf.name,
        package_version=build_conf.version,
        maintainer=build_conf.pkg_branch.maintainer,
        description=build_conf.get_fisheye_link
    )
    if depends_list:
        controlfile_content += "Depends: {depends}\n".format(depends=", ".join(depends_list))

    controlfile.write(controlfile_content)
    os.chmod("%s/DEBIAN/control" % PACKAGE_NAME, 0775)
    controlfile.close()

    # Create preinstall script
    if build_conf.pre_install_script:
        preinstfile = open("%s/DEBIAN/preinst" % PACKAGE_NAME, "w")
        preinstfile.write(str(build_conf.pre_install_script.replace("\r", "")))
        preinstfile.close()
        os.chmod("%s/DEBIAN/preinst" % PACKAGE_NAME, 0775)

    # Create postinstall script
    if build_conf.post_install_script:
        postinstfile = open("%s/DEBIAN/postinst" % PACKAGE_NAME, "w")
        postinstfile.write(str(build_conf.post_install_script.replace("\r", "")))
        postinstfile.close()
        os.chmod("%s/DEBIAN/postinst" % PACKAGE_NAME, 0775)

    # Run build package
    build_output = commands.getoutput("dpkg-deb --build {package_name} {branch_dir_path}/{package_name}_all.deb".format(
        package_name=PACKAGE_NAME,
        branch_dir_path=build_conf.pkg_branch.path
    ))

    build_conf.build_log = build_output
    build_conf.last_build_date = datetime.datetime.now()

    os.chdir(settings.TMP_BUILD_DIR)

    if re.search("dpkg-deb: building package.*in", build_output):
        build_conf.status = 3
        logging.info("Build package %s done." % PACKAGE_NAME)
        shutil.rmtree(settings.TMP_BUILD_DIR + "/" + PKG_BUILD_DIR)
    else:
        build_conf.status = 4
        logging.error(build_output)

    build_conf.save()

    return True


def run_remote_script(build_conf_id):
    build_conf = BuildConfiguration.objects.get(pk=build_conf_id)

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=str(build_conf.remote_ip),
            username=build_conf.ssh_user,
            password=build_conf.ssh_pass,
            port=int(build_conf.ssh_port)
        )

        stdin, stdout, stderr = client.exec_command(str(build_conf.build_script).replace("\r", ""))
        build_conf.build_log = stdout.read() + stderr.read()
        build_conf.last_build_date = datetime.datetime.now()
        client.close()
    except Exception as e:
        stop_by_error(build_conf, e)
        return False

    build_conf.status = 3
    build_conf.save()

    return True


@shared_task
def start_build(build_conf_id, current_id=None):
    build_conf = BuildConfiguration.objects.get(pk=build_conf_id)

    print("Package %s updates. Run rebuild task." % build_conf.name)

    build_conf.status = 2
    build_conf.version += 1

    if current_id:
        build_conf.last_commit_id = current_id

    build_conf.save()

    if build_conf.pkg_branch_id == 1:
        return run_remote_script(build_conf.pk)
    else:
        return build_pkg(build_conf.pk)


@shared_task
def autobuild():
    """
    Run rebuild package tasks
    on git commit
    """

    for build_conf in BuildConfiguration.objects.filter(auto_build=True):
        current_id = get_ref_id(build_conf)
        if not current_id:
            stop_by_error(build_conf, "Can't get last commit ID. Please check GIT url, login info / branch name.")
            continue
        if build_conf.last_commit_id != current_id:
            start_build(build_conf.pk, current_id)
            for rel_build_conf in BuildConfiguration.objects.filter(build_on_commit_in=build_conf):
                start_build(rel_build_conf.pk)
