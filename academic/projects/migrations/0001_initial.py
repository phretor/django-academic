# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Topic'
        db.create_table('projects_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('highlight', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('highlight_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('excerpt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('projects', ['Topic'])

        # Adding model 'Project'
        db.create_table('projects_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('highlight', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('redirect_to', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=1024, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('excerpt', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('footer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['projects.Topic'])),
        ))
        db.send_create_signal('projects', ['Project'])

        # Adding M2M table for field downloads on 'Project'
        db.create_table('projects_project_downloads', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('download', models.ForeignKey(orm['academic.download'], null=False))
        ))
        db.create_unique('projects_project_downloads', ['project_id', 'download_id'])

        # Adding M2M table for field people on 'Project'
        db.create_table('projects_project_people', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('person', models.ForeignKey(orm['people.person'], null=False))
        ))
        db.create_unique('projects_project_people', ['project_id', 'person_id'])

        # Adding M2M table for field organizations on 'Project'
        db.create_table('projects_project_organizations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('organization', models.ForeignKey(orm['organizations.organization'], null=False))
        ))
        db.create_unique('projects_project_organizations', ['project_id', 'organization_id'])

        # Adding M2M table for field publications on 'Project'
        db.create_table('projects_project_publications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('publication', models.ForeignKey(orm['publishing.publication'], null=False))
        ))
        db.create_unique('projects_project_publications', ['project_id', 'publication_id'])

        # Adding M2M table for field sponsors on 'Project'
        db.create_table('projects_project_sponsors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('sponsor', models.ForeignKey(orm['organizations.sponsor'], null=False))
        ))
        db.create_unique('projects_project_sponsors', ['project_id', 'sponsor_id'])

        # Adding M2M table for field related_topics on 'Project'
        db.create_table('projects_project_related_topics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('topic', models.ForeignKey(orm['projects.topic'], null=False))
        ))
        db.create_unique('projects_project_related_topics', ['project_id', 'topic_id'])


    def backwards(self, orm):
        
        # Deleting model 'Topic'
        db.delete_table('projects_topic')

        # Deleting model 'Project'
        db.delete_table('projects_project')

        # Removing M2M table for field downloads on 'Project'
        db.delete_table('projects_project_downloads')

        # Removing M2M table for field people on 'Project'
        db.delete_table('projects_project_people')

        # Removing M2M table for field organizations on 'Project'
        db.delete_table('projects_project_organizations')

        # Removing M2M table for field publications on 'Project'
        db.delete_table('projects_project_publications')

        # Removing M2M table for field sponsors on 'Project'
        db.delete_table('projects_project_sponsors')

        # Removing M2M table for field related_topics on 'Project'
        db.delete_table('projects_project_related_topics')


    models = {
        'academic.download': {
            'Meta': {'ordering': "['title']", 'object_name': 'Download'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'db_index': 'True', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'web_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'organizations.sponsor': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Sponsor', '_ormbases': ['organizations.Organization']},
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['organizations.Organization']", 'unique': 'True', 'primary_key': 'True'})
        },
        'people.person': {
            'Meta': {'ordering': "['rank', 'last_name', 'first_name']", 'object_name': 'Person'},
            'affiliation': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['organizations.Organization']"}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'e_mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'mid_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'picture': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'to': "orm['people.Rank']"}),
            'web_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'people.rank': {
            'Meta': {'ordering': "['order']", 'object_name': 'Rank'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'projects.project': {
            'Meta': {'ordering': "['topic', 'modified', 'created']", 'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'downloads': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['academic.Download']", 'null': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'footer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['organizations.Organization']"}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': "orm['people.Person']"}),
            'publications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['publishing.Publication']", 'null': 'True', 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'related_topics': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_projects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['projects.Topic']"}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['organizations.Sponsor']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['projects.Topic']"})
        },
        'projects.topic': {
            'Meta': {'ordering': "['highlight_order', 'title']", 'object_name': 'Topic'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'highlight_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'})
        },
        'publishing.publication': {
            'Meta': {'ordering': "['year']", 'object_name': 'Publication'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'attachment': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'publications'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['people.Person']"}),
            'bibtex': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'citation_key': ('django.db.models.fields.SlugField', [], {'max_length': '512', 'db_index': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'fulltext': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'})
        }
    }

    complete_apps = ['projects']
