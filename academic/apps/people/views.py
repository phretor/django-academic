# for some reason, switching to class-based views causes crazy things
# with {{ object_list|regroup }}. Thus, let's stick to the old
# approach for now.
'''
from django.views.generic.list import ListView

from academic.people.models import Person

class PeopleListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(PeopleListView, self).get_context_data(**kwargs)
        context['alumni'] = Person.objects_alumni.all()
        context['visitors'] = Person.objects_visitors.all()
        context['past_visitors'] = Person.objects_past_visitors.all()
        return context
'''
