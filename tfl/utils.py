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


def validate_number(number):
    try:
        float(number)
    except ValueError as e:
        raise TflError(e)
    else:
        return number


def validate_boolean(_bool):
    if isinstance(_bool, bool):
        return _bool
    elif _bool.lower() in ["t", "true"]:
        return True
    elif _bool.lower() in ["f", "false"]:
        return False
    else:
        raise TflError("\"{0}\" is not a valid boolean".format(_bool))
