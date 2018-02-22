#! /usr/bin/env python


class TflError(Exception):

    @property
    def message(self):
        return self.args[0]
