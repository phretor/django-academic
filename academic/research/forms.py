from django import forms

from research.models import *

from bibstuff import bibfile

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class PaperAdminForm(forms.ModelForm):
    class Meta:
        model = Paper

    def clean_bibtex(self):
        buf = StringIO.StringIO()
        bfile = BibFile()
        try:
            bibgrammar.Parse(buf, bfile)
        except:
            bfile = None
        buf.close()
        if bfile:
            if len(bfile.entries) > 0:
                self.cleaned_data['bibtex'] = bfile.entries[0]
        return self.cleaned_data['bibtex']
