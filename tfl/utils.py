# -*- coding: utf-8 -*-
import re
from datetime import date


def validate_year(year):
    year_re = re.compile('(|19|20)\d{2}$')
    if not year_re.match(year):
        return False

    now = date.today().year
    if int(year) > now:
        return False

    return True
