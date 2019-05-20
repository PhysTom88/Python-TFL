#! /usr/bin/env python


class TflError(Exception):
    """A Generic error from TfL"""
    pass

class HttpMethodNotAllowed(Exception):
    """This method does not allow that HTTP method"""
    pass

class InvalidInputError(TypeError):
    """This input is in the wrong format"""
    pass

class HttpResponseError(Exception):
    """An error in the HTTP Response"""
    pass
