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
    def fromJSON(cls, data, **kwargs):
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


class AdditionalProperty(TflModel):

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
        return "AdditionalProperty(Key={0}, Value={1})".format(
            self.key, self.value)

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


class Point(TflModel):

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
        return "Point(ID={0}, CommonName={1})".format(
            self.id, self.commonName
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        additional_properties = None
        children = None
        children_urls = None

        if 'additionalProperties' in data:
            additional_properties = [
                AdditionalProperty.fromJSON(bp)
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


class JourneyMode(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "isTflService": False,
            "isFarePaying": False,
            "isScheduledService": False,
            "modeName": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyMode(ModeName={0})".format(self.modeName)


class Place(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "naptanId": None,
            "modes": None,
            "icsCode": None,
            "stopType": None,
            "url": None,
            "commonName": None,
            "placeType": None,
            "additionalProperties": None,
            "lat": None,
            "lon": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Place(ID={0}, CommonName={1})".format(
            self.naptanId, self.commonName)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        modes = None
        additional_properties = None
        if "modes" in data:
            modes = [mode for mode in data["modes"]]
        if "additionalProperties" in data:
            additional_properties = [
                AdditionalProperty(p) for p in data["additionalProperties"]]

        return super(cls, cls).fromJSON(
            data=data, modes=modes, additionalProperties=additional_properties)


class DisambiguationOption(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "parameterValue": None,
            "uri": None,
            "place": None,
            "matchQuality": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "DisambiguationOption(ID={0}, MatchQuality={1})".format(
            self.parameterValue, self.matchQuality
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        place = None
        if "place" in data:
            place = Place.fromJSON(data["place"])

        return super(cls, cls).fromJSON(data=data, place=place)


class LocationDisambiguation(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "disambiguationOptions": None,
            "matchStatus": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "LocationDisambiguation(Status={0})".format(self.matchStatus)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        options = None
        if "disambiguationOptions" in data:
            options = [
                DisambiguationOption.fromJSON(d)
                for d in data["disambiguationOptions"]]

        return super(cls, cls).fromJSON(
            data=data, disambiguationOptions=options)


class Adjustment(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "date": None,
            "time": None,
            "timeIs": None,
            "uri": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Adjustment(Date={0}, Time={1}, TimeIs={2})".format(
            self.date, self.time, self.timeIs
        )


class TimeAdjustments(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "earliest": None,
            "earlier": None,
            "later": None,
            "latest": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        "TimeAdjustments(Earliest={0}, Latest={1})".format(
            getattr(self.earliest, "date", None),
            getattr(self.latest, "date", None)
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        earliest = None
        earlier = None
        later = None
        latest = None
        if "earliest" in data:
            earliest = Adjustment.fromJSON(data["earliest"])
        if "earlier" in data:
            earlier = Adjustment.fromJSON(data["earlier"])
        if "later" in data:
            later = Adjustment.fromJSON(data["later"])
        if "latest" in data:
            latest = Adjustment.fromJSON(data["latest"])

        return super(cls, cls).fromJSON(
            data=data, earliest=earliest, earlier=earlier,
            later=later, latest=latest)


class JourneySearch(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "dateTime": None,
            "dateTimeType": None,
            "timeAdjustments": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneySearch(DateTime={0}, Type={1})".format(
            self.dateTime, self.dateTimeType
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        time_adjustments = None
        if "timeAdjustments" in data:
            time_adjustments = TimeAdjustments.fromJSON(
                data["timeAdjustments"]
            )

        return super(cls, cls).fromJSON(
            data=data, timeAdjustments=time_adjustments)


class JourneyOutline(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "_from": None,
            "to": None,
            "via": None,
            "uri": None
        }

        for (param, default) in self.defaults.items():
            # We need to avoid the reserved keyword here
            kwarg_value = param
            if param == "_from":
                kwarg_value = "from"
            setattr(self, param, kwargs.get(kwarg_value, default))

    def __repr__(self):
        return "JourneyOutline(From={0}, To={1}, Via={2})".format(
            self._from, self.to, self.via
        )


class JourneyDisambiguation(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "toLocationDisambiguation": None,
            "fromLocationDisambiguation": None,
            "viaLocationDisambiguation": None,
            "recommendedMaxAgeMinutes": None,
            "searchCriteria": None,
            "journeyVector": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyDisambiguation(From={0}, To={1})".format(
            getattr(self.journeyVector, "_from", None),
            getattr(self.journeyVector, "to", None)
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        to_location = None
        from_location = None
        via_location = None
        search_criteria = None
        journey_vector = None

        if "toLocationDisambiguation" in data:
            to_location = LocationDisambiguation.fromJSON(
                data["toLocationDisambiguation"])
        if "fromLocationDisambiguation" in data:
            from_location = LocationDisambiguation.fromJSON(
                data["fromLocationDisambiguation"])
        if "viaLocationDisambiguation" in data:
            via_location = LocationDisambiguation.fromJSON(
                data["viaLocationDisambiguation"])
        if "searchCriteria" in data:
            search_criteria = JourneySearch.fromJSON(data["searchCriteria"])
        if "journeyVector" in data:
            journey_vector = JourneyOutline.fromJSON(data["journeyVector"])

        return super(cls, cls).fromJSON(
            data=data, toLocationDisambiguation=to_location,
            fromLocationDisambiguation=from_location,
            viaLocationDisambiguation=via_location,
            searchCriteria=search_criteria, journeyVector=journey_vector)


class JourneyLegObstacle(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "position": None,
            "type": None,
            "incline": None,
            "stopId": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyLegObstacle(ID={0}, Type={1}, Incline={2})".format(
            self.stopId, self.type, self.incline
        )


class JourneyLegPlannedWorks(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "id": None,
            "description": None,
            "createdDateTime": None,
            "lastUpdateDateTime": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyLegPlannedWorks(ID={0})".format(self.id)


class JourneyStepPathAttribute(TflModel):

    def __init__(self, **kwargs):

        self.defaults = {
            "value": None,
            "name": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyStepPathAttribute(Name={0}, Value={1}".format(
            self.name, self.value
        )


class JourneyLegInstructionStep(TflModel):

    def __init__(self, **kwargs):

        self.defaults = {
            "description": None,
            "turnDirection": None,
            "streetName": None,
            "distance": None,
            "cumulativeDistance": None,
            "skyDirection": None,
            "skyDirectionDescription": None,
            "cumulativeTravelTime": None,
            "latitude": None,
            "longitude": None,
            "pathAttribute": None,
            "descriptionHeading": None,
            "trackType": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return ("JourneyLegInstructionStep(SkyDirection={0}, "
                "StreetName={1})".format(
                    self.skyDirection, self.streetName)
                )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        pathAttribute = None
        if "pathAttribute" in data:
            pathAttribute = JourneyStepPathAttribute.fromJSON(
                data["pathAttribute"]
            )

        return super(cls, cls).fromJSON(data=data, pathAttribute=pathAttribute)


class JourneyLegInstruction(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "detailed": None,
            "steps": None,
            "summary": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyLegInstruction(Summary={0})".format(self.summary)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        steps = None

        if "steps" in data:
            steps = [
                JourneyLegInstructionStep.fromJSON(s) for s in data["steps"]]

        return super(cls, cls).fromJSON(data=data, steps=steps)


class Location(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "lat": None,
            "lon": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Location(Lat={0}, Lon={1})".format(self.lat, self.lon)


class PassengerFlow(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "timeSlice": None,
            "value": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "PassengerFlow(Time={0}, Value={1})".format(
            self.timeSlice, self.value
        )


class TrainLoading(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "line": None,
            "lineDirection": None,
            "platformDirection": None,
            "direction": None,
            "naptanTo": None,
            "timeSlice": None,
            "value": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "TrainLoading(Line={0}, To={1})".format(
            self.line, self.naptanTo
        )


class Crowding(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "passengerFlows": None,
            "trainLoadings": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Crowding(Loading={0}, Flow={1})".format(
            self.trainLoadings, self.passengerFlows
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        passengerFlows = None
        trainLoadings = None

        if "passengerFlows" in data:
            passengerFlows = [
                PassengerFlow.fromJSON(p) for p in data["passengerFlows"]
            ]
        if "trainLoadings" in data:
            trainLoadings = [
                TrainLoading.fromJSON(t) for t in data["trainLoadings"]
            ]

        return super(cls, cls).fromJSON(
            data=data, passengerFlows=passengerFlows,
            trainLoadings=trainLoadings
        )


class LineSequence(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "id": None,
            "name": None,
            "uri": None,
            "fullName": None,
            "type": None,
            "crowding": None,
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        "LineSequence(ID={0}, Name={1})".format(self.id, self.name)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        crowding = None

        if "crowding" in data and isinstance(data["crowding"], list):
            crowding = [Crowding.fromJSON(c) for c in data["crowding"]]
        elif "crowding" in data and isinstance(data["crowding"], dict):
            crowding = Crowding.fromJSON(data["crowding"])

        return super(cls, cls).fromJSON(data=data, crowding=crowding)


class LineGroup(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "naptanIdReference": None,
            "stationAtcoCode": None,
            "lineIdentifier": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        "LineGroup(ID={0})".format(self.naptanIdReference)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        lineIdentifier = None

        if "lineIdentifier" in data:
            lineIdentifier = [l for l in data["lineIdentifier"]]

        return super(cls, cls).fromJSON(
            data=data, lineIdentifier=lineIdentifier
        )


class LineModeGroup(TflModel):

    def __init___(self, **kwargs):
        self.defaults = {
            "modeName": None,
            "lineIdentifier": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "LineModeGroup(Mode={0})".format(self.modeName)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        lineIdentifier = None

        if "lineIdentifier" in data:
            lineIdentifier = [l for l in data["lineIdentifier"]]

        return super(cls, cls).fromJSON(
            data=data, lineIdentifier=lineIdentifier
        )


class StopPoint(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "naptanId": None,
            "platformName": None,
            "indicator": None,
            "stopLetter": None,
            "modes": None,
            "icsCode": None,
            "smsCode": None,
            "stopType": None,
            "stationNaptan": None,
            "accessibilitySummary": None,
            "hubNaptanCode": None,
            "lines": None,
            "lineGroup": None,
            "lineModeGroups": None,
            "fullName": None,
            "naptanMode": None,
            "status": None,
            "id": None,
            "url": None,
            "commonName": None,
            "distance": None,
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
        "StopPoint(ID={0}, FullName={1})".format(self.id, self.fullName)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        modes = None
        lines = None
        lineGroup = None
        lineModeGroups = None
        additionalProperties = None
        children = None
        childrenUrls = None

        if "modes" in data:
            modes = [mode for mode in data["modes"]]
        if "lines" in data:
            lines = [LineSequence.fromJSON(l) for l in data["lines"]]
        if "lineGroup" in data:
            lineGroup = [LineGroup.fromJSON(g) for g in data["lineGroup"]]
        if "lineModeGroups" in data:
            lineModeGroups = [
                LineModeGroup.fromJSON(m) for m in data["lineModeGroups"]
            ]
        if "additionalProperties" in data:
            additionalProperties = [
                AdditionalProperty.fromJSON(p)
                for p in data["additionalProperties"]
            ]
        if "children" in data:
            children = [Point.fromJSON(c) for c in data["children"]]
        if "childrenUrls" in data:
            childrenUrls = [u for u in data["childrenUrls"]]

        return super(cls, cls).fromJSON(
            data=data, modes=modes, lines=lines, lineGroup=lineGroup,
            lineModeGroups=lineModeGroups,
            additionalProperties=additionalProperties,
            children=children, childrenUrls=childrenUrls
        )


class RouteSequence(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "ordinal": None,
            "stopPoint": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        "RouteSequence(Ordinal={0})".format(self.ordinal)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        stopPoint = None

        if "stopPoint" in data:
            stopPoint = StopPoint.fromJSON(data["stopPoint"])

        return super(cls, cls).fromJSON(data=data, stopPoint=stopPoint)


class AffectedRoute(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "id": None,
            "lineId": None,
            "routeCode": None,
            "name": None,
            "lineString": None,
            "direction": None,
            "originationName": None,
            "destinationName": None,
            "validFrom": None,
            "validTo": None,
            "routeSectionNaptanEntrySequence": None,
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "AffectedRoute(ID={0}, Name={1})".format(
            self.id, self.name
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        route_sequence = None

        if "routeSectionNaptanEntrySequence" in data:
            route_sequence = [
                RouteSequence.fromJSON(r)
                for r in data["routeSectionNaptanEntrySequence"]]

        return super(cls, cls).fromJSON(
            data=data, routeSectionNaptanEntrySequence=route_sequence
        )


class Disruption(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "category": None,
            "type": None,
            "categoryDescription": None,
            "description": None,
            "summary": None,
            "additionalInfo": None,
            "created": None,
            "lastUpdate": None,
            "affectedRoutes": None,
            "affectedStops": None,
            "closureText": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Disruption(Category={0}, Created={1})".format(
            self.category, self.created
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        affected_routes = None
        affected_stops = None

        if "affectedRoutes" in data:
            affected_routes = [
                AffectedRoute.fromJSON(a) for a in data["affectedRoutes"]]
        if "affectedStops" in data:
            affected_stops = [
                StopPoint.fromJSON(s) for s in data["affectedStops"]]

        return super(cls, cls).fromJSON(
            data=data, affectedRoutes=affected_routes,
            affectedStops=affected_stops)


class RouteOption(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "directions": None,
            "name": None,
            "lineIdentifier": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "RouteOption(name={0})".format(self.name)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        directions = None
        lineIdentifier = None

        if "directions" in data:
            directions = [d for d in data["directions"]]
        if "lineIdentifier" in data:
            lineIdentifier = LineSequence.fromJSON(data["lineIdentifier"])

        return super(cls, cls).fromJSON(
            data=data, directions=directions, lineIdentifier=lineIdentifier)


class Elevation(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "distance": None,
            "startLat": None,
            "startLon": None,
            "endLat": None,
            "endLon": None,
            "heightFromPreviousPoint": None,
            "gradient": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Elevation(Start=({0}, {1}), End=({0}, {1}))".format(
            self.startLat, self.startLon, self.endLat, self.endLon
        )


class JourneyPath(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "lineString": None,
            "elevation": None,
            "stopPoints": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyPath()"

    @classmethod
    def fromJSON(cls, data, **kwargs):
        elevation = None
        stopPoints = None

        if "elevation" in data:
            elevation = [
                Elevation.fromJSON(e) for e in data["elevation"]
            ]
        if "stopPoints" in data:
            stopPoints = [LineSequence.fromJSON(l) for l in data["stopPoints"]]

        return super(cls, cls).fromJSON(
            data, elevation=elevation, stopPoints=stopPoints
        )


class JourneyLeg(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "departureTime": None,
            "obstacles": None,
            "plannedWorks": None,
            "arrivalPoint": None,
            "departurePoint": None,
            "instruction": None,
            "isDisrupted": None,
            "disruptions": None,
            "routeOptions": None,
            "mode": None,
            "arrivalTime": None,
            "duration": None,
            "path": None,
            "hasFixedLocations": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyLeg(From={0}, To={1}, IsDisrupted={2}".format(
            self.departurePoint, self.arrivalPoint, self.isDisrupted
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        obstacles = None
        plannedWorks = None
        instruction = None
        arrivalPoint = None
        departurePoint = None
        disruptions = None
        routeOptions = None
        mode = None
        path = None

        if "obstacles" in data:
            obstacles = [
                JourneyLegObstacle.fromJSON(ob) for ob in data["obstacles"]]
        if "plannedWorks" in data:
            plannedWorks = [
                JourneyLegPlannedWorks.fromJSON(p)
                for p in data["plannedWorks"]
            ]
        if "instruction" in data:
            instruction = JourneyLegInstruction.fromJSON(data["instruction"])
        if "arrivalPoint" in data:
            arrivalPoint = Location.fromJSON(data["arrivalPoint"])
        if "departurePoint" in data:
            departurePoint = Location.fromJSON(data["departurePoint"])
        if "disruptions" in data:
            disruptions = [Disruption.fromJSON(d) for d in data["disruptions"]]
        if "routeOptions" in data:
            routeOptions = [
                RouteOption.fromJSON(r) for r in data["routeOptions"]
            ]
        if "mode" in data:
            mode = LineSequence.fromJSON(data["mode"])
        if "path" in data:
            path = JourneyPath.fromJSON(data["path"])
        return super(cls, cls).fromJSON(
            data=data, obstacles=obstacles, plannedWorks=plannedWorks,
            instruction=instruction, arrivalPoint=arrivalPoint,
            departurePoint=departurePoint, disruptions=disruptions,
            routeOptions=routeOptions, mode=mode, path=path)


class Journey(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "duration": None,
            "legs": None,
            "startDateTime": None,
            "arrivalDateTime": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Journey(Duration={0}, StartTime={1}, ArrivalTime={2})".format(
            self.duration, self.startDateTime, self.arrivalDateTime
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        legs = None

        if "legs" in data:
            legs = [JourneyLeg.fromJSON(l) for l in data["legs"]]

        return super(cls, cls).fromJSON(data=data, legs=legs)


class ValidityPeriod(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "fromDate": None,
            "toDate": None,
            "isNow": False
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "ValidityPeriod(From={0}, To={1})".format(
            self.fromDate, self.toDate
        )


class LineStatus(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "id": None,
            "lineId": None,
            "statusSeverity": None,
            "statusSeverityDescription": None,
            "reason": None,
            "created": None,
            "modified": None,
            "validityPeriods": None,
            "disruption": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "LineStatus(ID={0}, LineID={1})".format(self.id, self.lineId)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        validityPeriods = None
        disruptions = None

        if "validityPeriods" in data:
            validityPeriods = [
                ValidityPeriod.fromJSON(v) for v in data["validityPeriods"]
            ]
        if "disruptions" in data:
            disruptions = [
                Disruption.fromJSON(d) for d in data["disruptions"]
            ]

        return super(cls, cls).fromJSON(
            data=data, validityPeriods=validityPeriods,
            disruptions=disruptions
        )


class RouteSection(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "routeCode": None,
            "name": None,
            "direction": None,
            "originationName": None,
            "destinationName": None,
            "originator": None,
            "destination": None,
            "serviceType": None,
            "validTo": None,
            "validFrom": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "RouteSection(RouteCode={0}, name={1})".format(
            self.routeCode, self.name
        )


class ServiceType(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "name": None,
            "uri": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "ServiceType(Name={0})".format(self.name)


class Line(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "id": None,
            "name": None,
            "modeName": None,
            "disruptions": None,
            "created": None,
            "modified": None,
            "lineStatuses": None,
            "routeSections": None,
            "serviceTypes": None,
            "crowding": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Line(ID={0}, Name={1})".format(self.id, self.name)

    @classmethod
    def fromJSON(cls, data, **kwargs):
        disruptions = None
        lineStatuses = None
        routeSections = None
        serviceTypes = None
        crowding = None

        if "disruptions" in data:
            disruptions = [Disruption.fromJSON(d) for d in data["disruptions"]]
        if "lineStatuses" in data:
            lineStatuses = [
                LineStatus.fromJSON(l) for l in data["lineStatuses"]
            ]
        if "routeSections" in data:
            routeSections = [
                RouteSection.fromJSON(r) for r in data["routeSections"]
            ]
        if "serviceTypes" in data:
            serviceTypes = [
                ServiceType.fromJSON(s) for s in data["serviceTypes"]
            ]
        if "crowding" in data:
            crowding = Crowding.fromJSON(data["crowding"])

        return super(cls, cls).fromJSON(
            data=data, disruptions=disruptions, lineStatuses=lineStatuses,
            routeSections=routeSections, serviceTypes=serviceTypes,
            crowding=crowding
        )


class DockingPoint(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "originNumberOfBikes": None,
            "destinationNumberOfBikes": None,
            "originNumberOfEmptySlots": None,
            "destinationNumberOfEmptySlots": None,
            "originId": None,
            "destinationId": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "DockingPoint(ID={0}, NoBikes={1})".format(
            self.originId, self.originNumberOfBikes
        )


class JourneyPlanner(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "journeyVector": None,
            "journeys": None,
            "lines": None,
            "searchCriteria": None,
            "stopMessages": None,
            "recommendedMaxAgeMinutes": None,
            "cycleHireDockingStationData": None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "JourneyPlanner(From={0}, To={1})".format(
            getattr(self.journeyVector, "_from", None),
            getattr(self.journeyVector, "to", None)
        )

    @classmethod
    def fromJSON(cls, data, **kwargs):
        journeys = None
        journey_vector = None
        lines = None
        search_criteria = None
        stop_messages = None
        docking_data = None

        if "journeys" in data:
            journeys = [Journey.fromJSON(j) for j in data["journeys"]]
        if "journeyVector" in data:
            journey_vector = JourneyOutline.fromJSON(data["journeyVector"])
        if "lines" in data:
            lines = [Line.fromJSON(l) for l in data["lines"]]
        if "searchCriteria" in data:
            search_criteria = JourneySearch.fromJSON(data["searchCriteria"])
        if "stopMessages" in data:
            stop_messages = [message for message in data["stopMessages"]]
        if "cycleHireDockingStationData" in data:
            docking_data = DockingPoint.fromJSON(
                data["cycleHireDockingStationData"]
            )

        return super(cls, cls).fromJSON(
            data=data, journeys=journeys, journeyVector=journey_vector,
            lines=lines, searchCriteria=search_criteria,
            cycleHireDockingStationData=docking_data,
            stopMessages=stop_messages)


class LineStatusSeverity(TflModel):

    def __init__(self, **kwargs):
        self.defaults = {
            "modeName": None,
            "severityLevel": None,
            "description": None,
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "LineStatusSeverity(ModeName={0}, SeverityLevel={1})".format(
            self.modeName, self.severityLevel
        )
