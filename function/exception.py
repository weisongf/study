#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Invalid(CinderException):
    message = _("Unacceptable parameters.")
    code = 400


class InvalidBackup(Invalid):
    message = _("Invalid backup: %(reason)s")