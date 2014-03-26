from django.db import models
from django.conf import settings

STATUS_CHOICE = (
    (0, "None"),
    (1, "Pending"),
    (2, "In progress"),
    (3, "Success"),
    (4, "Error"),
)


class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    path = models.CharField(max_length=300, blank=True, null=True)
    maintainer = models.CharField(max_length=300, verbose_name="User Name <user@mail.tld>")
    is_virtual = models.BooleanField()

    def __unicode__(self):
        return self.name


class BuildConfiguration(models.Model):
    name = models.CharField(max_length=255)
    version = models.IntegerField(default=0, blank=True)
    status = models.IntegerField(default=0, blank=True, choices=STATUS_CHOICE)
    last_build_date = models.DateTimeField(blank=True, null=True)
    last_commit_id = models.CharField(max_length=100, null=True, blank=True)
    git_url = models.URLField()
    git_user = models.CharField(max_length=100)
    git_pass = models.CharField(max_length=100)
    git_branch = models.CharField(max_length=100)
    auto_build = models.BooleanField(default=False, blank=True)
    build_script = models.TextField(null=True, blank=True)
    build_log = models.TextField(null=True, blank=True)
    build_on_commit_in = models.ManyToManyField('BuildConfiguration', blank=True, null=True)
    pkg_branch = models.ForeignKey(Branch, blank=True, null=True)
    install_root = models.CharField(max_length=255)
    pre_install_script = models.TextField(null=True, blank=True)
    post_install_script = models.TextField(null=True, blank=True)
    depends_list = models.TextField(null=True, blank=True)
    remote_ip = models.CharField(max_length=100, null=True, blank=True)
    ssh_user = models.CharField(max_length=32, null=True, blank=True)
    ssh_pass = models.CharField(max_length=255, blank=True, null=True)
    ssh_port = models.IntegerField(max_length=7, blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def get_repo_name(self):
        try:
            repo_name = self.git_url.split("/")[-1].split(".")[0]
        except:
            repo_name = None
        return repo_name

    @property
    def get_fisheye_link(self):
        if not settings.FISHEYE_LINK:
            return None
        else:
            return "{fisheye_link}/fisheye/changelog/{repo_name}?showid={revision_id}".format(
                fisheye_link=settings.FISHEYE_LINK,
                repo_name=self.get_repo_name,
                revision_id=self.last_commit_id
            )


class PackageNameMapping(models.Model):
    orig_name = models.CharField(max_length=255, unique=True)
    to_name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return "%s => %s" % (self.orig_name, self.to_name)