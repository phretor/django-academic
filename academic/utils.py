from datetime import date
from django.utils.dates import MONTHS as _MONTHS

YEARS = map(lambda x: (str(x), str(x)), range(1960, date.today().year + 10))
MONTHS = map(lambda x: (x[0], x[1]), _MONTHS.items())
