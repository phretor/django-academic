# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Organization'
        db.create_table('organizations_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('web_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(db_index=True, max_length=2, null=True, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal('organizations', ['Organization'])

        # Adding model 'Institution'
        db.create_table('organizations_institution', (
            ('organization_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['organizations.Organization'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('organizations', ['Institution'])

        # Adding model 'School'
        db.create_table('organizations_school', (
            ('organization_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['organizations.Organization'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('organizations', ['School'])

        # Adding model 'Publisher'
        db.create_table('organizations_publisher', (
            ('organization_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['organizations.Organization'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('organizations', ['Publisher'])

        # Adding model 'Sponsor'
        db.create_table('organizations_sponsor', (
            ('organization_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['organizations.Organization'], unique=True, primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('logo', self.gf('filebrowser.fields.FileBrowseField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('organizations', ['Sponsor'])


    def backwards(self, orm):
        
        # Deleting model 'Organization'
        db.delete_table('organizations_organization')

        # Deleting model 'Institution'
        db.delete_table('organizations_institution')

        # Deleting model 'School'
        db.delete_table('organizations_school')

        # Deleting model 'Publisher'
        db.delete_table('organizations_publisher')

        # Deleting model 'Sponsor'
        db.delete_table('organizations_sponsor')


    models = {
        'organizations.institution': {
            'Meta': {'object_name': 'Institution', '_ormbases': ['organizations.Organization']},
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['organizations.Organization']", 'unique': 'True', 'primary_key': 'True'})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'db_index': 'True', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'web_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'organizations.publisher': {
            'Meta': {'object_name': 'Publisher', '_ormbases': ['organizations.Organization']},
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['organizations.Organization']", 'unique': 'True', 'primary_key': 'True'})
        },
        'organizations.school': {
            'Meta': {'object_name': 'School', '_ormbases': ['organizations.Organization']},
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['organizations.Organization']", 'unique': 'True', 'primary_key': 'True'})
        },
        'organizations.sponsor': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Sponsor', '_ormbases': ['organizations.Organization']},
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['organizations.Organization']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['organizations']
