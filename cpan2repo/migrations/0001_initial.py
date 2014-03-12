# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Package'
        db.create_table(u'cpan2repo_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
        ))
        db.send_create_signal(u'cpan2repo', ['Package'])

        # Adding model 'ExcludePackage'
        db.create_table(u'cpan2repo_excludepackage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cpan2repo', ['ExcludePackage'])


    def backwards(self, orm):
        # Deleting model 'Package'
        db.delete_table(u'cpan2repo_package')

        # Deleting model 'ExcludePackage'
        db.delete_table(u'cpan2repo_excludepackage')


    models = {
        u'cpan2repo.excludepackage': {
            'Meta': {'object_name': 'ExcludePackage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cpan2repo.package': {
            'Meta': {'object_name': 'Package'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['cpan2repo']