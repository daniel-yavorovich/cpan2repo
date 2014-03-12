# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Branch'
        db.create_table(u'webui_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('maintainer', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'webui', ['Branch'])

        # Adding model 'BuildConfiguration'
        db.create_table(u'webui_buildconfiguration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('last_build_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('git_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('git_user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('git_pass', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('git_branch', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pkg_branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webui.Branch'])),
            ('auto_build', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('install_root', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pre_install_script', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('post_install_script', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('depends_list', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('build_log', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'webui', ['BuildConfiguration'])

        # Adding model 'PackageNameMapping'
        db.create_table(u'webui_packagenamemapping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orig_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('to_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'webui', ['PackageNameMapping'])


    def backwards(self, orm):
        # Deleting model 'Branch'
        db.delete_table(u'webui_branch')

        # Deleting model 'BuildConfiguration'
        db.delete_table(u'webui_buildconfiguration')

        # Deleting model 'PackageNameMapping'
        db.delete_table(u'webui_packagenamemapping')


    models = {
        u'webui.branch': {
            'Meta': {'object_name': 'Branch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintainer': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'webui.buildconfiguration': {
            'Meta': {'object_name': 'BuildConfiguration'},
            'auto_build': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'build_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'depends_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'git_branch': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'git_pass': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'git_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'git_user': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_root': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_build_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pkg_branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webui.Branch']"}),
            'post_install_script': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pre_install_script': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'webui.packagenamemapping': {
            'Meta': {'object_name': 'PackageNameMapping'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'to_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['webui']