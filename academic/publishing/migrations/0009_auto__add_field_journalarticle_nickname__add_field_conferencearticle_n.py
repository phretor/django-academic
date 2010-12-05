# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'JournalArticle.nickname'
        db.add_column('publishing_journalarticle', 'nickname', self.gf('django.db.models.fields.SlugField')(default='concept-drift', max_length=32, db_index=True), keep_default=False)

        # Adding field 'ConferenceArticle.nickname'
        db.add_column('publishing_conferencearticle', 'nickname', self.gf('django.db.models.fields.SlugField')(default='concept-drift', max_length=32, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'JournalArticle.nickname'
        db.delete_column('publishing_journalarticle', 'nickname')

        # Deleting field 'ConferenceArticle.nickname'
        db.delete_column('publishing_conferencearticle', 'nickname')


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
        'publishing.advisorship': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Advisorship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.Thesis']"})
        },
        'publishing.authorship': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Authorship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.Publication']"})
        },
        'publishing.book': {
            'Meta': {'ordering': "['-year']", 'object_name': 'Book', '_ormbases': ['publishing.Publication']},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'proceedings'", 'to': "orm['people.Person']", 'through': "orm['publishing.Editorship']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'publication_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Publication']", 'unique': 'True', 'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'books'", 'null': 'True', 'to': "orm['organizations.Publisher']"}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'publishing.bookchapter': {
            'Meta': {'ordering': "['-year']", 'object_name': 'BookChapter', '_ormbases': ['publishing.Book']},
            'book_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Book']", 'unique': 'True', 'primary_key': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'publishing.coadvisorship': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Coadvisorship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.Thesis']"})
        },
        'publishing.conference': {
            'Meta': {'ordering': "['acronym', 'name']", 'object_name': 'Conference'},
            'acronym': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'})
        },
        'publishing.conferencearticle': {
            'Meta': {'ordering': "['-year']", 'object_name': 'ConferenceArticle', '_ormbases': ['publishing.Publication']},
            'crossref': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.ConferenceProceedings']", 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'presentation': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publication_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Publication']", 'unique': 'True', 'primary_key': 'True'})
        },
        'publishing.conferenceedition': {
            'Meta': {'ordering': "['-year', '-month', 'conference__acronym', 'conference__name']", 'unique_together': "(('conference', 'year'),)", 'object_name': 'ConferenceEdition'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.Conference']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '512', 'db_index': 'True'}),
            'web_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'})
        },
        'publishing.conferenceproceedings': {
            'Meta': {'ordering': "['-year']", 'object_name': 'ConferenceProceedings', '_ormbases': ['publishing.Book']},
            'book_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Book']", 'unique': 'True', 'primary_key': 'True'}),
            'conference_edition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.ConferenceEdition']"})
        },
        'publishing.editorship': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Editorship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.Book']"})
        },
        'publishing.journal': {
            'Meta': {'ordering': "['-year']", 'object_name': 'Journal', '_ormbases': ['publishing.Book']},
            'book_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Book']", 'unique': 'True', 'primary_key': 'True'})
        },
        'publishing.journalarticle': {
            'Meta': {'ordering': "['-year']", 'object_name': 'JournalArticle', '_ormbases': ['publishing.Publication']},
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.Journal']"}),
            'nickname': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'publication_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Publication']", 'unique': 'True', 'primary_key': 'True'})
        },
        'publishing.masterthesis': {
            'Meta': {'ordering': "['-year']", 'object_name': 'MasterThesis', '_ormbases': ['publishing.Thesis']},
            'thesis_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Thesis']", 'unique': 'True', 'primary_key': 'True'})
        },
        'publishing.phdthesis': {
            'Meta': {'ordering': "['-year']", 'object_name': 'PhdThesis', '_ormbases': ['publishing.Thesis']},
            'reviewers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'reviewed_phdtheses'", 'to': "orm['people.Person']", 'through': "orm['publishing.Reviewing']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'thesis_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Thesis']", 'unique': 'True', 'primary_key': 'True'})
        },
        'publishing.publication': {
            'Meta': {'ordering': "['-year']", 'unique_together': "(('title', 'year'),)", 'object_name': 'Publication'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'attachment': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'publications'", 'to': "orm['people.Person']", 'through': "orm['publishing.Authorship']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'bibtex': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'fulltext': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '512', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'})
        },
        'publishing.reviewing': {
            'Meta': {'object_name': 'Reviewing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.PhdThesis']"})
        },
        'publishing.technicalreport': {
            'Meta': {'ordering': "['-year']", 'object_name': 'TechnicalReport', '_ormbases': ['publishing.Publication']},
            'institution': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['organizations.Institution']", 'symmetrical': 'False'}),
            'publication_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Publication']", 'unique': 'True', 'primary_key': 'True'})
        },
        'publishing.thesis': {
            'Meta': {'ordering': "['-year']", 'object_name': 'Thesis', '_ormbases': ['publishing.Publication']},
            'advisors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'advised_theses'", 'symmetrical': 'False', 'through': "orm['publishing.Advisorship']", 'to': "orm['people.Person']"}),
            'co_advisors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'coadvised_theses'", 'to': "orm['people.Person']", 'through': "orm['publishing.Coadvisorship']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'publication_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Publication']", 'unique': 'True', 'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.School']"})
        }
    }

    complete_apps = ['publishing']
