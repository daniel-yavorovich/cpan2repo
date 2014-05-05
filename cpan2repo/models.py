# -*- coding: utf-8 -*-
from django.db import models

STATUSES_CHOICE = (
    (1, u"Pending"),
    (2, u"In progress"),
    (3, u"Installed"),
)


class Package(models.Model):
    name = models.CharField(max_length=200)
    status = models.IntegerField(choices=STATUSES_CHOICE, default=1, blank=True)

    def __unicode__(self):
        return self.name


class ExcludePackage(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name