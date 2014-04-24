import json
from django.contrib.auth.decorators import login_required
from cpan2repo.tasks import start_build
from django.shortcuts import render, get_object_or_404
from webui.models import Branch, BuildConfiguration, PackageNameMapping
from django.http import HttpResponseRedirect, HttpResponse
from webui.forms import BranchForm, BuildConfigurationForm, PackageNameMappingForm, RemoteBuildConfigurationForm


# Build configurations views
@login_required
def index(request):
    return render(request, 'index.html', {
    }, content_type="text/html")


def branches(request):
    return HttpResponse(
        json.dumps(
            list(Branch.objects.values("pk", "name", "path", "maintainer", "is_virtual"))
        ),
        content_type="application/json"
    )


def build_confs(request):
    return HttpResponse(
        json.dumps(
            list(BuildConfiguration.objects.values("pk", "name", "pkg_branch__name", "version", "status",
                                                   "last_build_date", "auto_build"))
        ),
        content_type="application/json"
    )


def mapping(request):
    return HttpResponse(
        json.dumps(
            list(PackageNameMapping.objects.values("pk", "orig_name", "to_name"))
        ),
        content_type="application/json"
    )


@login_required
def rebuild_package(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)
    build_conf.status = 3
    build_conf.save()
    try:
        start_build.delay(build_conf.pk)
        message = {
            "level": "success",
            "text": 'Task for rebuild package "%s" in branch "%s" sent.' % (build_conf.name, build_conf.pkg_branch),
        }
    except Exception as e:
        message = {
            "level": "danger",
            "text": 'Error send task for build package "%s" in branch "%s: %s".' % (
                build_conf.name, build_conf.pkg_branch, e)
        }

    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


@login_required
def autobuild_on_off(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)
    build_conf.auto_build = not build_conf.auto_build
    build_conf.save()

    return HttpResponse(
        json.dumps({"autobuild_status": build_conf.auto_build}),
        content_type="application/json"
    )


@login_required
def remove_build_conf(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)
    message = {
        "level": "success",
        "text": "Package '%s' from branch '%s' removed!" % (build_conf.name, build_conf.pkg_branch)
    }
    build_conf.delete()

    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


@login_required
def remove_branch(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    message = {
        "level": "success",
        "text": "Branch '%s' removed!" % (branch.name)
    }
    branch.delete()

    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


@login_required
def remove_mapping(request, mapping_id):
    mapping = get_object_or_404(PackageNameMapping, pk=mapping_id)
    message = {
        "level": "success",
        "text": "Mapping '%s -> %s' removed!" % (mapping.orig_name, mapping.to_name)
    }
    mapping.delete()

    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


@login_required
def add_build_conf(request, conf_type="deb"):
    print conf_type
    if conf_type == "remote":
        build_conf_form = RemoteBuildConfigurationForm
    else:
        build_conf_form = BuildConfigurationForm

    if request.method == "POST":
        form = build_conf_form(request.POST, initial={"conf_type": conf_type})
    else:
        form = build_conf_form(initial={"conf_type": conf_type})

    if form.is_valid():
        build_conf = form.save()
        if conf_type == "remote":
            # Set Remote Build virtual branch
            build_conf.pkg_branch = Branch.objects.get(pk=1)
            build_conf.save()
        return HttpResponseRedirect("/")

    return render(request, 'edit_form.html', {
        'form': form,
        'title': "Add Build Configuration",
        'current_page': 'build_conf',
    }, content_type="text/html")


@login_required
def edit_build_conf(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)

    if build_conf.pkg_branch_id == 1:
        build_conf_form = RemoteBuildConfigurationForm
    else:
        build_conf_form = BuildConfigurationForm

    if request.method == "POST":
        form = build_conf_form(request.POST, instance=build_conf)
    else:
        form = build_conf_form(instance=build_conf)

    del form.fields["conf_type"]

    if form.is_valid():
        build_conf = form.save()
        return HttpResponseRedirect("/")

    return render(request, 'edit_form.html', {
        'form': form,
        'current_page': 'build_conf',
        'title': "Change Build Configuration: %s" % build_conf.name,
    }, content_type="text/html")


@login_required
def view_log(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)

    return render(request, 'view_log.html', {
        'current_page': 'build_conf',
        'build_conf': build_conf,
    }, content_type="text/html")


@login_required
def rebuild_all_packages(request):
    try:
        for build_conf in BuildConfiguration.objects.all():
            start_build.delay(build_conf.pk)
    except:
        pass

    return HttpResponseRedirect("/")


# Branches views
@login_required
def add_branch(request):
    if request.method == "POST":
        form = BranchForm(request.POST)
    else:
        form = BranchForm()

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/#/branches')

    return render(request, 'edit_form.html', {
        'form': form,
        'title': "Add Branch",
        'current_page': 'branch',
    }, content_type="text/html")


@login_required
def edit_branch(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    if request.method == "POST":
        form = BranchForm(request.POST, instance=branch)
    else:
        form = BranchForm(instance=branch)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/#/branches')

    return render(request, 'edit_form.html', {
        'form': form,
        'current_page': 'branch',
        'title': "Change Branch Configuration: %s" % branch.name,
    }, content_type="text/html")


@login_required
def add_mapping(request):
    if request.method == "POST":
        form = PackageNameMappingForm(request.POST)
    else:
        form = PackageNameMappingForm()

    if form.is_valid():
        mapping = form.save()
        return HttpResponseRedirect("/#/mapping")

    return render(request, 'edit_form.html', {
        'form': form,
        'title': "Add Mapping",
        'current_page': 'mapping',
    }, content_type="text/html")


@login_required
def edit_mapping(request, mapping_id):
    mapping = get_object_or_404(PackageNameMapping, pk=mapping_id)
    if request.method == "POST":
        form = PackageNameMappingForm(request.POST, instance=mapping)
    else:
        form = PackageNameMappingForm(instance=mapping)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/#/mapping")

    return render(request, 'edit_form.html', {
        'form': form,
        'current_page': 'mapping',
        'title': "Change Mapping Configuration: %s => %s" % (mapping.orig_name, mapping.to_name),
    }, content_type="text/html")