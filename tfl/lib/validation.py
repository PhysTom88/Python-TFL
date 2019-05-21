# -*- coding: utf-8 -*-
import re
from datetime import date, datetime

from tfl.api.exceptions import TflError, InvalidInputError


def validate_year(year):
    clean_year = validate_input(year, str, "year")
    year_re = re.compile('(|19|20)\d{2}$')
    if not year_re.match(clean_year):
        raise InvalidInputError("\"{0}\" is in an invalid format".format(clean_year))

    now = date.today().year
    if int(year) > now:
        raise InvalidInputError("\"{0}\" is not an accepted value".format(clean_year))

    return clean_year


def validate_input(_input, _type, var):
    try:
        _value = _type(_input)
    except ValueError:
        raise TflError("\"{0}\" is not of type {1}".format(var, _type.__str__()))
    else:
        return _value

def validate_latitude(lat):
    clean_lat = validate_input(lat, float, "latitude")
    if not (-90 <= clean_lat <= 90):
        raise InvalidInputError("Latitude out of range")

    return clean_lat


def validate_longitude(longitude):
    clean_long = validate_input(longitude, float, "longitude")
    if not (-180 <= clean_long <= 180):
        raise InvalidInputError("Longitude out of range")

    return clean_long


def validate_datestring(date, string_format, length=None):
    clean_date = validate_input(date, str, "date")
    if length and len(clean_date) != length:
        raise InvalidInputError("Invalid date format, must be '{0}'".format(string_format))
    try:
        datetime.strptime(clean_date, string_format)
    except ValueError:
        raise InvalidInputError("Invalid date format, must be '{0}'".format(string_format))
    else:
        return clean_date
