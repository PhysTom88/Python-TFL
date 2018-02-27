# -*- coding: utf-8 -*-
import re
from datetime import date

from tfl.exceptions import TflError


def validate_year(year):
    year_re = re.compile('(|19|20)\d{2}$')
    if not year_re.match(str(year)):
        raise TflError("\"{0}\" is in an invalid format".format(year))

    now = date.today().year
    if int(year) > now:
        raise TflError("\"{0}\" is not an accepted value".format(year))

    return str(year)


def validate_input(_input, _type, var):
    try:
        _value = _type(_input)
    except ValueError:
        raise TflError("\"{0}\" is not of type {1}".format(var.__name__))
    else:
        return _value
