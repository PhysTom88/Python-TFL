# -*- coding: utf-8 -*-
from tfl.api import Api
from tfl.lib.validation import validate_input, validate_datestring


class Journey(Api):

    ALLOWED_TIME_IS = ["departing", "arriving"]
    ALLOWED_JOURNEY_PREFERENCE = ["Leastinterchange", "Leastwalking", "leasttime"]

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
            alternative_walking=None, use_multi_modal_call=None,
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
        if time_is in self.ALLOWED_JOURNEY_PREFERENCE:
            extra_params["timeis"] = time_is
        if journey_preference in self.ALLOWED_JOURNEY_PREFERENCE:
            extra_params["journeyPreference"] = journey_preference
        if mode is not None:
            if isinstance(mode, (tuple, list)):
                extra_params["mode"] = ','.join(
                    [validate_input(m, str, "mode") for m in mode])
            else:
                extra_params["mode"] = validate_input(mode, str, "mode")
