# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BuildConfiguration.remote_ip'
        db.add_column(u'webui_buildconfiguration', 'remote_ip',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BuildConfiguration.ssh_user'
        db.add_column(u'webui_buildconfiguration', 'ssh_user',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BuildConfiguration.ssh_pass'
        db.add_column(u'webui_buildconfiguration', 'ssh_pass',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BuildConfiguration.ssh_port'
        db.add_column(u'webui_buildconfiguration', 'ssh_port',
                      self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field build_on_commit_in on 'BuildConfiguration'
        m2m_table_name = db.shorten_name(u'webui_buildconfiguration_build_on_commit_in')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_buildconfiguration', models.ForeignKey(orm[u'webui.buildconfiguration'], null=False)),
            ('to_buildconfiguration', models.ForeignKey(orm[u'webui.buildconfiguration'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_buildconfiguration_id', 'to_buildconfiguration_id'])


        # Changing field 'BuildConfiguration.pkg_branch'
        db.alter_column(u'webui_buildconfiguration', 'pkg_branch_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webui.Branch'], null=True))
        # Adding field 'Branch.is_virtual'
        db.add_column(u'webui_branch', 'is_virtual',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Branch.path'
        db.alter_column(u'webui_branch', 'path', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

    def backwards(self, orm):
        # Deleting field 'BuildConfiguration.remote_ip'
        db.delete_column(u'webui_buildconfiguration', 'remote_ip')

        # Deleting field 'BuildConfiguration.ssh_user'
        db.delete_column(u'webui_buildconfiguration', 'ssh_user')

        # Deleting field 'BuildConfiguration.ssh_pass'
        db.delete_column(u'webui_buildconfiguration', 'ssh_pass')

        # Deleting field 'BuildConfiguration.ssh_port'
        db.delete_column(u'webui_buildconfiguration', 'ssh_port')

        # Removing M2M table for field build_on_commit_in on 'BuildConfiguration'
        db.delete_table(db.shorten_name(u'webui_buildconfiguration_build_on_commit_in'))


        # Changing field 'BuildConfiguration.pkg_branch'
        db.alter_column(u'webui_buildconfiguration', 'pkg_branch_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['webui.Branch']))
        # Deleting field 'Branch.is_virtual'
        db.delete_column(u'webui_branch', 'is_virtual')


        # Changing field 'Branch.path'
        db.alter_column(u'webui_branch', 'path', self.gf('django.db.models.fields.CharField')(default=None, max_length=300))

    models = {
        u'webui.branch': {
            'Meta': {'object_name': 'Branch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_virtual': ('django.db.models.fields.BooleanField', [], {}),
            'maintainer': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'webui.buildconfiguration': {
            'Meta': {'object_name': 'BuildConfiguration'},
            'auto_build': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'build_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'build_on_commit_in': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['webui.BuildConfiguration']", 'null': 'True', 'blank': 'True'}),
            'build_script': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'depends_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'git_branch': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'git_pass': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'git_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'git_user': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_root': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_build_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_commit_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pkg_branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webui.Branch']", 'null': 'True', 'blank': 'True'}),
            'post_install_script': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pre_install_script': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'remote_ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ssh_pass': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ssh_port': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'ssh_user': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
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