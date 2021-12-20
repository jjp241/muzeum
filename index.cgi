#!/usr/bin/python3

from wsgiref.handlers import CGIHandler

from index import app

CGIHandler().run(app)

