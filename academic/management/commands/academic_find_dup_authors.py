from django.core.management.base import BaseCommand, CommandError
from academic.people.models import Person
from django.utils.encoding import smart_unicode, smart_str

from optparse import make_option

class Command(BaseCommand):
    help = 'Finds duplicate authors based on first/last name correspondence'

    def handle(self, *args, **options):
	idx = {}
	for p in Person.objects_all.all():
	    try:
	        idx[p.first_name + ' ' + p.last_name].append(p)
	    except KeyError:
	        idx[p.first_name + ' ' + p.last_name] = [p]
	for n,l in idx.iteritems():
	    if len(l) > 1:
	        self.stdout.write('\n%s\n' % n)
	        self.stdout.write('-' * len(n) + '\n')
	        for p in l:
		    self.stdout.write('\tID %s %s %s %s %s %s ' % (p.id, p.first_name, p.mid_name, p.last_name, p.e_mail, p.web_page))
		    if p.publications.all().count() > 0:
			self.stdout.write('(cannot be safely deleted: see following publications)\n'.upper())
			for r in p.publications.all():
			    self.stdout.write('\t\tID %d %s %s\n' % (r.id, smart_str(r.year), smart_str(r.title)))
		    else:
			self.stdout.write('(may be deleted: no publications found, but please double check)\n'.upper())
