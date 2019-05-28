# -*- coding: utf-8 -*-
from tfl.api import Api
from tfl.lib.validation import validate_input, validate_datestring


class Journey(Api):

    ALLOWED_TIME_IS = ["departing", "arriving"]
    JOURNEY_PREFERENCE = ["Leastinterchange", "Leastwalking", "leasttime"]
    ACCESSIBILITY_PREFERENCE = ["noSolidStairs", "noEscalators", "noElavators",
                                        "stepFreeToVehicle", "stepFreeToPlatform"]
    WALKING_SPEEDS = ["slow", "average", "fast"]
    CYCLE_PREFERENCE = ["AllTheWay", "LeaveAtStation", "TakeOnTransport", "CycleHire"]
    TRIP_ADJUSTMENT = ["TripFirst", "TripLast"]
    CYCLE_PROFICIENCY = ["easy", "moderate", "fast"]

    def journey_planner_modes(self):
        url = self.base_url + "Journey/Meta/Modes/"
        response = self._request(url, http_method="GET")
        data = self._check_response(response.json())

        return data

    def journey_planner_search(
            self, _from, to, via=None, national_search=False, date=None,
            time=None, time_is=None, journey_preference=None, mode=None,
            accessibility_preference=None, from_name=None, to_name=None,
            via_name=None, max_transfer_minutes=None, max_walking_minutes=None,
            walking_speed=None, cycle_preference=None, adjustment=None,
            bike_proficiency=None, alternative_cycle=None,
            alternative_walking=None, apply_html=None, use_multi_modal_call=None,
            walking_optimsation=False, taxi_only_trip=False
    ):
        url = self.base_url + "Journey/JourneyResults/{0}/to/{1}"
        extra_params = dict()

        if via is not None:
            extra_params["via"] = validate_input(via, str, "via")
        if national_search is not None:
            extra_params["nationalSearch"] = validate_input(
                national_search, bool, "national_search"
            )
        if date is not None:
            extra_params["date"] = validate_datestring(date, string_format="%Y%m%d", length=8)
        if time is not None:
            extra_params["time"] = validate_datestring(time, string_format="%H:%M")
        if time_is in self.JOURNEY_PREFERENCE:
            extra_params["timeis"] = time_is
        if journey_preference in self.JOURNEY_PREFERENCE:
            extra_params["journeyPreference"] = journey_preference
        if mode is not None:
            if isinstance(mode, (tuple, list)):
                extra_params["mode"] = ','.join(
                    [validate_input(m, str, "mode") for m in mode])
            else:
                extra_params["mode"] = validate_input(mode, str, "mode")
        if accessibility_preference in self.ACCESSIBILITY_PREFERENCE:
            extra_params["accessibilityPreference"] = accessibility_preference
        if from_name is not None:
            extra_params["fromName"] = validate_input(from_name, str, "from_name")
        if to_name is not None:
            extra_params["toName"] = validate_input(to_name, str, "to_name")
        if via_name is not None:
            extra_params["viaName"] = validate_input(via_name, str, "via_name")
        if max_transfer_minutes is not None:
            extra_params["maxTransferMinutes"] = str(validate_input(max_transfer_minutes, int, "max_transfer_minutes"))
        if max_walking_minutes is not None:
            extra_params["maxWalkingMinutes"] = str(validate_input(max_walking_minutes, int, "max_walking_minutes"))
        if walking_speed in self.WALKING_SPEEDS:
            extra_params["walkingSpeed"] = walking_speed
        if cycle_preference in self.CYCLE_PREFERENCE:
            extra_params["cyclePreference"] = cycle_preference
        if adjustment in self.TRIP_ADJUSTMENT:
            extra_params["adjustment"] = adjustment
        if bike_proficiency in self.CYCLE_PROFICIENCY:
            extra_params["bikeProficiency"] = bike_proficiency
        if alternative_cycle is not None:
            extra_params["alternativeCycle"] = validate_input(alternative_cycle, bool, "alternative_cycle")
        if alternative_walking is not None:
            extra_params["alternativeCycle"] = validate_input(alternative_walking, bool, "alternative_walking")
        if apply_html is not None:
            extra_params["applyHTMLMarker"] = validate_input(apply_html, bool, "apply_html")
        if use_multi_modal_call is not None:
            extra_params["useMultiModalCall"] = validate_input(use_multi_modal_call, bool, "use_multi_modal_call")
        if walking_optimsation is not None:
            extra_params["walkingOptimsation"] = validate_input(walking_optimsation, bool, "walking_optimisation")
        if taxi_only_trip is not None:
            extra_params["taxiOnlyTrip"] = validate_input(taxi_only_trip, bool, "taxi_only_trip")

        response = self._request(
            url.format(
                validate_input(_from, str, "_from"),
                validate_input(to, str, "to")),
            extra_params=extra_params, http_method="GET")
        data = self._check_response(
            response.json()
        )

        return data
