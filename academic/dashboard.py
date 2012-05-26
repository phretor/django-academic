from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard

class CustomIndexDashboard(Dashboard):
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.children.extend([
                modules.ModelList(
                    title=_('People and organizations'),
                    column=1,
                    models=[
                        'academic.people.*',
                        'academic.organizations.*',],
                    ),
                modules.ModelList(
		    title=_('Publishing'),
                    column=1,
		    models=['academic.publishing.*',],
                    ),
                modules.ModelList(
		    title=_('Projects'),
                    column=1,
		    models=('academic.projects.*',),
                    ),
		modules.LinkList(
		    title=_('Media Management'),
		    column=2,
		    children=[
			{
			    'title': _('Browse and upload files'),
			    'url': '/admin/filebrowser/browse/',
			    'external': False,
                            },
                        ]
                    ),
		modules.ModelList(
		    title=_('Content and pages'),
		    column=1,
		    models=[
			'academic.content.*',
			'django.contrib.flatpages.*',
			'flatcontent.*'],
                    ),
		modules.ModelList(
		    title=_('Administration'),
                    column=2,
		    models=[
			'django.contrib.auth.*',
			'django.contrib.sites.*'],
                    ),
		modules.Feed(
		    title=_(''),
                    column=3,
                    feed_url='http://www.djangoproject.com/rss/weblog/',
		    limit=5,
                    ),
		modules.RecentActions(
		    title='Recent actions',
                    column=2,
                    limit=5
                    ),
                ])
