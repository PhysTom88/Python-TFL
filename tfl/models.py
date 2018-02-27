# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dateutil import parser
import json


class TflModel(object):

    def __init__(self, **kwargs):
        self.defaults = {}

    def __str__(self):
        return self.toString()

    def __eq__(self, other):
        return other and self.toDict() == other.toDict()

    def __ne__(self, other):
        return not self.__eq__(other)

    def toString(self):
        return json.dumps(self.toDict(), sort_keys=True)

    def toDict(self):
        data = {}
        for (key, _) in self.defaults.items():
            if isinstance(getattr(self, key, None), (list, set, tuple)):
                data[key] = []
                for sub in getattr(self, key, None):
                    if getattr(sub, "toDict", None):
                        data[key].append(sub.toDict())
                    else:
                        data[key].append(sub)

            elif getattr(getattr(self, key, None), "toDict", None):
                data[key] = getattr(self, key).toDict()

            elif hasattr(self, key):
                data[key] = getattr(self, key, None)

        return data

    @classmethod
    def fromJSON(cls, data, **kwargs):
        json_data = data.copy()
        if kwargs:
            for k, v in kwargs.items():
                json_data[k] = v

        c = cls(**json_data)
        c._json = data

        return c


class Casualty(TflModel):

    def __init___(self, **kwargs):
        self.defaults = {
            "age": 0,
            "class": None,
            "severity": None,
            "mode": None,
            "ageBand": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Casualty(Age={0})".format(self.age)


class AccidentVehicle(TflModel):
    def __init__(self, **kwargs):
        self.defaults = {
            "type": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "AccidentVehicle(Type={0})".format(self.type)


class Accident(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "id": None,
            "lat": None,
            "lon": None,
            "date": None,
            "severity": None,
            "borough": None,
            "casualties": None,
            "vehicles": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Accident(ID={0}, Severity={1})".format(self.id, self.severity)

    @property
    def date_in_seconds(self):
        return int(parser.parse(self.date).strftime("%s"))

    @classmethod
    def fromJson(cls, data, **kwargs):
        casualties = None
        vehicles = None

        if 'casualties' in data:
            casualties = [Casualty.fromJSON(c) for c in data['casualties']]
        if 'vehicles' in data:
            vehicles = [AccidentVehicle.fromJSON(v) for v in data['vehicles']]

        return super(cls, cls).fromJSON(
            data=data, casualties=casualties, vehicles=vehicles)


class AirQuality(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "forecastType": None,
            "forecastID": None,
            "forecastBand": None,
            "forecastSummary": None,
            "nO2Band": None,
            "o3Band": None,
            "pM10Band": None,
            "pM25Band": None,
            "sO2Band": None,
            "forecastText": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "AirQuality(forecastID={0})".format(self.forecastID)


class BpProperty(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "category": None,
            "key": None,
            "sourceSystemKey": None,
            "value": None,
            "modified": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "BpProperty(Key={0}, Value={1})".format(self.key, self.value)

    @property
    def date_in_seconds(self):
        return int(parser.parse(self.modified).strftime("%s"))


class BpChildUrl(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "type": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "BpChildUrl(Type={0})".format(self.type)


class BikePoint(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "id": None,
            "url": None,
            "commonName": None,
            "distance": 0,
            "placeType": None,
            "additionalProperties": None,
            "children": None,
            "childrenUrls": None,
            "lat": None,
            "lon": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "BikePoint(ID={0}, CommonName={1})".format(
            self.id, self.commonName
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        additional_properties = None
        children = None
        children_urls = None

        if 'additionalProperties' in data:
            additional_properties = [
                BpProperty.fromJSON(bp)
                for bp in data['additionalProperties']]
        if 'children' in data:
            children = [c for c in data['children']]
        if 'childrenUrls' in data:
            children_urls = [
                BpChildUrl.fromJSON(cu) for cu in data['childrenUrls']]

        return super(cls, cls).fromJSON(
            data=data, additionalProperties=additional_properties,
            children=children, childrenUrls=children_urls)


class Cabwise(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "OperatorId": 0,
            "OrganisationName": None,
            "TradingName": None,
            "AlsoKnownAs": None,
            "CentreId": None,
            "AddressLine1": None,
            "AddressLine2": None,
            "AddressLine3": None,
            "Town": None,
            "County": None,
            "Postcode": None,
            "BookingsPhoneNumber": None,
            "BookingsEmail": None,
            "PublicAccess": None,
            "PublicWaitingRoom": None,
            "WheelchairAccessible": None,
            "CreditDebitCard": None,
            "ChequeBankersCard": None,
            "AccountServicesAvailable": None,
            "HoursOfOperation24X7": None,
            "HoursOfOperationMonThu": None,
            "StartTimeMonThu": None,
            "EndTimeMonThu": None,
            "HoursOfOperationFri": None,
            "StartTimeFri": None,
            "EndTimeFri": None,
            "HoursOfOperationSat": None,
            "StartTimeSat": None,
            "EndTimeSat": None,
            "HoursOfOperationSun": None,
            "StartTimeSun": None,
            "EndTimeSun": None,
            "HoursOfOperationPubHol": None,
            "StartTimePubHol": None,
            "EndTimePubHol": None,
            "NumberOfVehicles": None,
            "NumberOfVehiclesWheelchair": None,
            "Longitude": None,
            "Latitude": None,
            "OperatorTypes": None,
            "Distance": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Cabwise(ID={0}, Name={1})".format(
            self.CentreId, self.TradingName
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        also_known_as = None
        operator_types = None

        if 'AlsoKnownAs' in data:
            also_known_as = [a for a in data["AlsoKnownAs"]]
        if 'OperatorTypes' in data:
            operator_types = [t for t in data["OperatorTypes"]]

        return super(cls, cls).fromJSON(
            data=data, AlsoKnownAs=also_known_as,
            OperatorTypes=operator_types
        )
