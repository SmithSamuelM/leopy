# -*- encoding: utf-8 -*-
"""
Ending Module

ReST endpoints

"""

import sys
import os
from collections import deque

import enum
import  time

try:
    import simplejson as json
except ImportError:
    import json

import datetime
import mimetypes

import arrow
import falcon
import libnacl

from ioflo.aid.sixing import *
from ioflo.aid import lodict
from ioflo.aid import timing
from ioflo.aid import classing
from ioflo.aio.http import httping
from ioflo.base import Deck
from ioflo.aid import getConsole

console = getConsole()

Events = Deck()  # module global Deck deque FIFO of events

STATIC_BASE_PATH = "/static"
DEFAULT_STATIC_BASE_PATH = "/"

AGENT_BASE_PATH = "/agent"
SERVER_BASE_PATH = "/server"
THING_BASE_PATH = "/thing"
ANON_MSG_BASE_PATH = "/anon"
DEMO_BASE_PATH = "/demo"


STREAM_BASE_PATH = "/stream"
HISTORY_BASE_PATH = "/history"
BLOB_BASE_PATH = "/blob"
RELAY_BASE_PATH = "/relay"
ERRORS_BASE_PATH = "/errors"
EVENTS_BASE_PATH = "/event"





class CORSMiddleware:
    """
    Adds CORS headers to all endpoints
    To be more restrictive change 'Access-Control-Allow-Origin' header
    """
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Max-Age:', '3600')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods',
                                   'PUT, GET, POST, DELETE, HEAD, OPTIONS')
        resp.set_header('Access-Control-Allow-Headers',
                                   'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, X-Auth-Token, Signature')


class StaticSink(object):
    """
    Class that provided Falcon sink endpoint for serving static files.
    converts paths that start with '/static/' to '/' with remainder attached
    This way can use /static/ in web app

    """
    def __init__(self, *pa, **kwa):
        super().__init__(*pa, **kwa)
        self.projectDirpath = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(
                        os.path.expanduser(__file__))))
        self.staticDirpath = os.path.join(self.projectDirpath, "static")

    def __call__(self, req, rep):
        path = req.path  # Falcon removes trailing "/" if any after non "/"
        splits = path.split("/")[1:]  # split and remove first split [""]
        if not splits[0]:  # empty split
            splits = splits[1:]  #remove empty
        if splits and splits[0] == "static":
            splits = splits[1:]  #remove static from front leave rest
        if not splits:  # not a static path return default
            filepath = "main.html"
        else:
            filepath = "/".join(splits)  # reattach
        filepath = os.path.join(self.staticDirpath, filepath)
        if not os.path.exists(filepath):
            raise falcon.HTTPError(falcon.HTTP_NOT_FOUND,
                            'Missing Resource',
                            'File "{}" not found or forbidden'.format(filepath))
        filetype = mimetypes.guess_type(filepath, strict=True)[0]  # get first guess
        rep.set_header("Content-Type", "{}; charset=UTF-8".format(filetype))
        rep.status = falcon.HTTP_200  # This is the default status
        # rep.stream = open(filepath, 'rb')  # bug connection never closes
        #  see if new req.bounded_stream works
        with open(filepath, 'rb') as f:
            rep.body = f.read()


class TopicSink(object):
    """
    Class that provides Falcon sink endpoint for controller topics
    Make sink callable for controller event topics
    """
    def __init__(self, *pa, **kwa):
        super().__init__(*pa, **kwa)

    def __call__(self, req, rep):
        """
        Handle all web hook state change event call backs
        Print to console request
        Respond with 200
        """
        try:  #  get raw data
            data = req.bounded_stream.read()

        except Exception:
            raise falcon.HTTPError(falcon.HTTP_748,
                                       'Read Error',
                                       'Could not read the request body.')

        console.terse("Sink: {} {}\n".format(req.relative_uri, req.method, data))

        try:  #  convert to json
            data = json.loads(data)
        except ValueError:
            console.terse("Raw:\n{}\n".format(data))
            raise falcon.HTTPError(falcon.HTTP_753,
                                       'Malformed JSON',
                                       'Could not decode the request body. The '
                                       'JSON was incorrect.')

        pre, sep, aft = req.path.partition("/topic/")
        topic = " ".join(aft.split("/")[:-1])
        event = dict(topic = topic)
        event["data"] = data

        console.terse("JSON:\n{}\n".format(json.dumps(event, indent=2)))
        Events.push(event)

        rep.status = falcon.HTTP_200  # This is the default status
        # rep.body = json.dumps(data)



# generator



class EventStreamResource:
    """
    Sever Sent Event stream of events Deck
    """
    def  __init__(self, store=None, **kwa):
        super(**kwa)
        self.store = store

    def eventGeneratorOneShot(self):
        """
        event generator one shot
        for testing with simple server or paw
        or client that has header connection close
        """
        while Events:
            event = Events.pull()
            console.terse("Streamed Event {}\n\n".format(event))
            yield bytes("{}\n".format(event), "ascii")

        # return generates StopeIteration which closes event stream


    def eventGenerator(self):
        """
        event generator persistent
        only works with ioflo server
        """
        sleepTimer = timing.StoreTimer(self.store, duration=0.5)

        yield bytes("retry: 500\n\n", "ascii") # Set client-side auto-reconnect timeout, ms.
        while (True):
            while Events:
                event = Events.pull()
                console.terse("Streamed Event: {}\n\n".format(event))
                yield bytes("data: {}\n\n".format(event), "ascii")

            sleepTimer.restart()
            while not sleepTimer.expired:
                yield bytes("", "ascii")  # yield empty is ignored not written
            # to close event stream return from generator to raise StopIteration

    def on_get(self, req, rep):
        """
        Handles GET requests
        """
        rep.status = falcon.HTTP_200  # This is the default status
        rep.content_type = "text/event-stream"
        rep.stream = self.eventGenerator()
        # rep.stream = self.eventGeneratorOneShot()





def loadEnds(app, store):
    """
    Load endpoints for app with store reference
    This function provides the endpoint resource instances
    with a reference to the data store

    :param app: falcon.API object
    :param store: Store
        ioflo datastore
    """
    staticSink = StaticSink()
    app.add_sink(staticSink, prefix=DEFAULT_STATIC_BASE_PATH)

    topicSink = TopicSink()
    app.add_sink(topicSink, '/topic/')

    eventStreamResource = EventStreamResource(store=store)
    app.add_route('/events', eventStreamResource)

