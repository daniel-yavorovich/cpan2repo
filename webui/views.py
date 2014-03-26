import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cpan2repo.tasks import build_pkg
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from webui.models import Branch, BuildConfiguration, PackageNameMapping
from django.http import HttpResponseRedirect, HttpResponse
from webui.forms import BranchForm, BuildConfigurationForm, PackageNameMappingForm, RemoteBuildConfigurationForm


# Build configurations views
@login_required
def index(request):
    branches = Branch.objects.exclude(buildconfiguration=None).order_by('-pk')
    remote_build_confs = BuildConfiguration.objects.filter(pkg_branch=None)

    return render(request, 'index.html', {
        'branches': branches,
        'remote_build_confs': remote_build_confs,
        'current_page': 'build_conf',
    }, content_type="text/html")


@login_required
def build_confs_list(request):
    build_confs = list(BuildConfiguration.objects.all().values('pk', 'name', 'version', 'status', 'last_build_date'))
    return HttpResponse(
        json.dumps(build_confs),
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
        messages.add_message(request, messages.SUCCESS, 'Build configuration "%s" created.' % build_conf.name)
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'edit_form.html', {
        'form': form,
        'title': "Add Build Configuration",
        'current_page': 'build_conf',
    }, content_type="text/html")


@login_required
def edit_build_conf(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)
    if request.method == "POST":
        form = BuildConfigurationForm(request.POST, instance=build_conf)
    else:
        form = BuildConfigurationForm(instance=build_conf)

    if form.is_valid():
        build_conf = form.save()
        messages.add_message(request, messages.SUCCESS, 'Build configuration "%s" saved.' % build_conf.name)

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
def remove_build_conf(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)
    build_conf.delete()

    return HttpResponse(status=204)


@login_required
def autobuild_on_off(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)
    build_conf.auto_build = not build_conf.auto_build
    build_conf.save()

    return HttpResponse(build_conf.auto_build)


@login_required
def rebuild_package(request, build_conf_id):
    build_conf = get_object_or_404(BuildConfiguration, pk=build_conf_id)
    try:
        build_pkg.delay(build_conf.pk)
        messages.add_message(request, messages.SUCCESS, 'Task for rebuild package "%s" in branch "%s" sent.' % (
            build_conf.name, build_conf.pkg_branch))
    except:
        messages.add_message(request, messages.ERROR,
                             'Internal error send task for build package "%s" in branch "%s".' % (
                             build_conf.name, build_conf.pkg_branch))

    return HttpResponseRedirect(reverse("index"))


@login_required
def rebuild_all_packages(request):
    try:
        for build_conf in BuildConfiguration.objects.all():
            build_pkg.delay(build_conf.pk)
        messages.add_message(request, messages.SUCCESS, 'Task for rebuild all packages sent.')
    except:
        messages.add_message(request, messages.ERROR, 'Internal error send task for rebuild all packages.')

    return HttpResponseRedirect(reverse("index"))


# Branches views

@login_required
def branches_list(request):
    branches = Branch.objects.all()

    return render(request, 'branches_list.html', {
        'branches': branches,
        'current_page': 'branch',
    }, content_type="text/html")


@login_required
def add_branch(request):
    if request.method == "POST":
        form = BranchForm(request.POST)
    else:
        form = BranchForm()

    if form.is_valid():
        branch = form.save()
        messages.add_message(request, messages.SUCCESS, 'Branch "%s" created.' % branch.name)
        return HttpResponseRedirect(reverse('branches_list'))

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
        branch = form.save()
        messages.add_message(request, messages.SUCCESS, 'Branch configuration "%s" saved.' % branch.name)

    return render(request, 'edit_form.html', {
        'form': form,
        'current_page': 'branch',
        'title': "Change Branch Configuration: %s" % branch.name,
    }, content_type="text/html")


@login_required
def rebuild_packages_by_branch(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    try:
        for build_conf in branch.buildconfiguration_set.all():
            build_pkg.delay(build_conf.pk)
        messages.add_message(request, messages.SUCCESS, 'Task for rebuild packages by branch "%s" sent.' % branch.name)
    except:
        messages.add_message(request, messages.ERROR,
                             'Internal error send task for rebuild packages by branch "%s".' % branch.name)

    return HttpResponseRedirect(reverse("index"))


@login_required
def remove_branch(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    branch.delete()

    return HttpResponse(status=204)


# Mapping views

@login_required
def mapping_list(request):
    mappings = PackageNameMapping.objects.all()

    return render(request, 'mappings_list.html', {
        'mappings': mappings,
        'current_page': 'mapping',
    }, content_type="text/html")


@login_required
def add_mapping(request):
    if request.method == "POST":
        form = PackageNameMappingForm(request.POST)
    else:
        form = PackageNameMappingForm()

    if form.is_valid():
        mapping = form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Mapping "%s => %s" created.' % (mapping.orig_name, mapping.to_name))
        return HttpResponseRedirect(reverse('mapping_list'))

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
        mapping = form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Mapping configuration "%s => %s" saved.' % (mapping.orig_name, mapping.to_name))

    return render(request, 'edit_form.html', {
        'form': form,
        'current_page': 'mapping',
        'title': "Change Mapping Configuration: %s => %s" % (mapping.orig_name, mapping.to_name),
    }, content_type="text/html")


@login_required
def remove_mapping(request, mapping_id):
    mapping = get_object_or_404(PackageNameMapping, pk=mapping_id)
    mapping.delete()

    return HttpResponse(status=204)