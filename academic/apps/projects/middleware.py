from django.http import HttpResponseRedirect

from academic.projects.models import Project

class ProjectRedirectMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'slug' in view_kwargs:
            try:
                object = Project.objects.get(slug=view_kwargs['slug'])                
		if object.redirect_to != '':
		    return HttpResponseRedirect(object.redirect_to)
            except Project.DoesNotExist:
		pass
        return None
