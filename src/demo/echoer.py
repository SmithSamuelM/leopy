# -*- encoding: utf-8 -*-
"""
Event Echo Server Module

ReST endpoints

"""

from collections import deque
import enum
import time
odict = dict


try:
    import simplejson as json
except ImportError:
    import json

import falcon


from ioflo.aid import getConsole
from ioflo.base import Deck

console = getConsole()

events = Deck()  # module global Deck deque FIFO of events



class EventResource:
    """
    Manages events deque of events.
    Get pulls earliest event
    Post pushs new event
    Put modifies latest event?
    """
    def  __init__(self, **kwa):
        super(**kwa)

    def on_get(self, req, rep):
        """
        Handles GET requests
        """

        try:
            event = events.pull()
        except IndexError:
            event = {}  #  empty event


        console.terse("GET {}\n\n".format(event))
        result = json.dumps(event)

        rep.status = falcon.HTTP_200  # This is the default status
        rep.body = result


    def on_put(self, req, rep):
        """
        Handles GET requests
        """
        console.terse("PUT {}\n\n".format(json.dumps(req.body)))
        result = {}

        rep.status = falcon.HTTP_200  # This is the default status
        rep.body = json.dumps(result)


    def on_post(self, req, rep):
        """
        Handles POST requests
        """
        try:  #  get raw data
            data = json.load(req.bounded_stream)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_753,
                                       'Malformed JSON',
                                       'Could not decode the request body. The '
                                       'JSON was incorrect.')
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_748,
                                       'Read Error',
                                       'Could not read the request body.')


        console.terse("POST: \n{}\n".format(data))
        events.push(data)


        #rep.status = falcon.HTTP_201
        #rep.location = '/example/%s' % (userId)  # location header redirect

        rep.status = falcon.HTTP_200  # This is the default status
        rep.body = json.dumps(data)

# generator
def eventGenerator():
    """
    event generator
    """
    while events:
        event = events.pull()
        console.terse("Streamed Event {}\n\n".format(event))
        yield bytes("{}\n".format(event), "ascii")
        time.sleep(0.1)
    yield bytes("{}\r\n".format({}), "ascii")  #  /r/n ends event stream


# generator
def foreverEventGenerator():
    """
    event generator
    """
    while (True):
        while events:
            event = events.pull()
            console.terse("Streamed Event {}\n\n".format(event))
            yield bytes("{}\n".format(event), "ascii")
            time.sleep(0.1)
        yield bytes("{}\n".format({}), "ascii")
        time.sleep(1.0)


class EventStreamResource:
    """
    Sever Sent Event stream of events Deck
    """
    def  __init__(self, **kwa):
        super(**kwa)

    def on_get(self, req, rep):
        """
        Handles GET requests
        """

        rep.status = falcon.HTTP_200  # This is the default status
        rep.content_type = "text/html"
        rep.stream = eventGenerator()





app = falcon.API() # falcon.API instances are callable WSGI apps

eventResource = EventResource()  # Resources are represented by long-lived class instances
app.add_route('/event', eventResource) # example handles all requests to '/example' URL path

eventStreamResource = EventStreamResource()
app.add_route('/events', eventStreamResource)



if __name__ == '__main__':
    from wsgiref import simple_server

    httpd = simple_server.make_server('127.0.0.1', 8080, app)
    httpd.serve_forever()  # navigate web client to http://127.0.0.1:8080/example
