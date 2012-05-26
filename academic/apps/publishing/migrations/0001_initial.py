# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Conference'
        db.create_table('publishing_conference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256, db_index=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
        ))
        db.send_create_signal('publishing', ['Conference'])

        # Adding model 'ConferenceEdition'
        db.create_table('publishing_conferenceedition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.Conference'])),
            ('edition_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('month', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, db_index=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('web_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=512, db_index=True)),
        ))
        db.send_create_signal('publishing', ['ConferenceEdition'])

        # Adding unique constraint on 'ConferenceEdition', fields ['conference', 'year']
        db.create_unique('publishing_conferenceedition', ['conference_id', 'year'])

        # Adding model 'Publication'
        db.create_table('publishing_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, db_index=True)),
            ('month', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('attachment', self.gf('filebrowser.fields.FileBrowseField')(max_length=256, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('bibtex', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fulltext', self.gf('filebrowser.fields.FileBrowseField')(max_length=256, null=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, db_index=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=512, db_index=True)),
        ))
        db.send_create_signal('publishing', ['Publication'])

        # Adding unique constraint on 'Publication', fields ['title', 'year']
        db.create_unique('publishing_publication', ['title', 'year'])

        # Adding model 'Authorship'
        db.create_table('publishing_authorship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.Publication'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('publishing', ['Authorship'])

        # Adding model 'Book'
        db.create_table('publishing_book', (
            ('publication_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Publication'], unique=True, primary_key=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='books', null=True, to=orm['organizations.Publisher'])),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('publishing', ['Book'])

        # Adding model 'Editorship'
        db.create_table('publishing_editorship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.Book'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('publishing', ['Editorship'])

        # Adding model 'Journal'
        db.create_table('publishing_journal', (
            ('book_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Book'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('publishing', ['Journal'])

        # Adding model 'BookChapter'
        db.create_table('publishing_bookchapter', (
            ('book_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Book'], unique=True, primary_key=True)),
            ('chapter', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal('publishing', ['BookChapter'])

        # Adding model 'JournalArticle'
        db.create_table('publishing_journalarticle', (
            ('publication_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Publication'], unique=True, primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.Journal'])),
        ))
        db.send_create_signal('publishing', ['JournalArticle'])

        # Adding model 'ConferenceProceedings'
        db.create_table('publishing_conferenceproceedings', (
            ('book_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Book'], unique=True, primary_key=True)),
            ('conference_edition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.ConferenceEdition'])),
        ))
        db.send_create_signal('publishing', ['ConferenceProceedings'])

        # Adding model 'ConferenceArticle'
        db.create_table('publishing_conferencearticle', (
            ('publication_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Publication'], unique=True, primary_key=True)),
            ('presentation', self.gf('filebrowser.fields.FileBrowseField')(max_length=256, null=True, blank=True)),
            ('crossref', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.ConferenceProceedings'], null=True, blank=True)),
        ))
        db.send_create_signal('publishing', ['ConferenceArticle'])

        # Adding model 'TechnicalReport'
        db.create_table('publishing_technicalreport', (
            ('publication_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Publication'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('publishing', ['TechnicalReport'])

        # Adding M2M table for field institution on 'TechnicalReport'
        db.create_table('publishing_technicalreport_institution', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('technicalreport', models.ForeignKey(orm['publishing.technicalreport'], null=False)),
            ('institution', models.ForeignKey(orm['organizations.institution'], null=False))
        ))
        db.create_unique('publishing_technicalreport_institution', ['technicalreport_id', 'institution_id'])

        # Adding model 'Thesis'
        db.create_table('publishing_thesis', (
            ('publication_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Publication'], unique=True, primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.School'])),
        ))
        db.send_create_signal('publishing', ['Thesis'])

        # Adding model 'Advisorship'
        db.create_table('publishing_advisorship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.Thesis'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('publishing', ['Advisorship'])

        # Adding model 'Coadvisorship'
        db.create_table('publishing_coadvisorship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.Thesis'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('publishing', ['Coadvisorship'])

        # Adding model 'MasterThesis'
        db.create_table('publishing_masterthesis', (
            ('thesis_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Thesis'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('publishing', ['MasterThesis'])

        # Adding model 'PhdThesis'
        db.create_table('publishing_phdthesis', (
            ('thesis_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['publishing.Thesis'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('publishing', ['PhdThesis'])

        # Adding model 'Reviewing'
        db.create_table('publishing_reviewing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.PhdThesis'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('publishing', ['Reviewing'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Publication', fields ['title', 'year']
        db.delete_unique('publishing_publication', ['title', 'year'])

        # Removing unique constraint on 'ConferenceEdition', fields ['conference', 'year']
        db.delete_unique('publishing_conferenceedition', ['conference_id', 'year'])

        # Deleting model 'Conference'
        db.delete_table('publishing_conference')

        # Deleting model 'ConferenceEdition'
        db.delete_table('publishing_conferenceedition')

        # Deleting model 'Publication'
        db.delete_table('publishing_publication')

        # Deleting model 'Authorship'
        db.delete_table('publishing_authorship')

        # Deleting model 'Book'
        db.delete_table('publishing_book')

        # Deleting model 'Editorship'
        db.delete_table('publishing_editorship')

        # Deleting model 'Journal'
        db.delete_table('publishing_journal')

        # Deleting model 'BookChapter'
        db.delete_table('publishing_bookchapter')

        # Deleting model 'JournalArticle'
        db.delete_table('publishing_journalarticle')

        # Deleting model 'ConferenceProceedings'
        db.delete_table('publishing_conferenceproceedings')

        # Deleting model 'ConferenceArticle'
        db.delete_table('publishing_conferencearticle')

        # Deleting model 'TechnicalReport'
        db.delete_table('publishing_technicalreport')

        # Removing M2M table for field institution on 'TechnicalReport'
        db.delete_table('publishing_technicalreport_institution')

        # Deleting model 'Thesis'
        db.delete_table('publishing_thesis')

        # Deleting model 'Advisorship'
        db.delete_table('publishing_advisorship')

        # Deleting model 'Coadvisorship'
        db.delete_table('publishing_coadvisorship')

        # Deleting model 'MasterThesis'
        db.delete_table('publishing_masterthesis')

        # Deleting model 'PhdThesis'
        db.delete_table('publishing_phdthesis')

        # Deleting model 'Reviewing'
        db.delete_table('publishing_reviewing')


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
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'presentation': ('filebrowser.fields.FileBrowseField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publication_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['publishing.Publication']", 'unique': 'True', 'primary_key': 'True'})
        },
        'publishing.conferenceedition': {
            'Meta': {'ordering': "['-year', '-month', 'conference__acronym', 'conference__name']", 'unique_together': "(('conference', 'year'),)", 'object_name': 'ConferenceEdition'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publishing.Conference']"}),
            'edition_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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
