/*
The EventSource object is used to receive server-sent event notifications:
Create a new EventSource object, and specify the URL of the page sending the updates (in this example "demo_sse.php")
Each time an update is received, the onmessage event occurs
 When an onmessage event occurs, put the received data into the element with id="result"
The EventSource Object
In the examples above we used the onmessage event to get messages. But other events are also available:

Event  Description
onopen  When a connection to the server is opened
onmessage  When a message is received
onerror  When an error occurs

https://www.w3.org/TR/eventsource/
https://www.html5rocks.com/en/tutorials/eventsource/basics/
https://auth0.com/blog/developing-real-time-web-applications-with-server-sent-events/
https://medium.com/conectric-networks/a-look-at-server-sent-events-54a77f8d6ff7

*/

// Declare an EventSource
const eventSource = new EventSource('http://some.url');
// Handler for events without an event type specified
eventSource.onmessage = (e) => {
  // Do something - event data etc will be in e.data
};
// Handler for events of type 'eventType' only
eventSource.addEventListener('eventType', (e) => {
  // Do something - event data will be in e.data,
  // message will be of type 'eventType'
});




if (!!window.EventSource) {
  var source = new EventSource('stream.php');
} else {
  // Result to xhr polling :(
}

source.addEventListener('message', function(e) {
  console.log(e.data);
}, false);

source.addEventListener('open', function(e) {
  // Connection was opened.
}, false);

source.addEventListener('error', function(e) {
  if (e.readyState == EventSource.CLOSED) {
    // Connection was closed.
  }
}, false);


var source = new EventSource("demo_sse.php");
source.onmessage = function(event) {
  document.getElementById("result").innerHTML += event.data + "<br>";
};


source.onerror = function(event) {
  console.log("EventSource failed.");
};

source.close();


var jrvs = jrvs || {};

jrvs.subscribe = function () {
  var source = new EventSource('/events');

  source.addEventListener('message', function (message) {
    var o = JSON.parse(message.data);

    if (typeof o === 'object' && Object.keys(o.body).length > 0) {
      var el = jrvs.widgetForJob(o.job);
      o.body.updatedAt = moment().format('HH:mm');
      jrvs.render(el, {data: o.body});
    }
  }, false);
};

jrvs.widgetForJob = function (name) {
  var el = document.querySelector('[data-job="' + name + '"]');
  // If no job is specified, assume job name == widget name
  if (el === null) {
    return document.querySelector('[data-widget="' + name + '"]');
  }
  return el;
};

jrvs.render = function (widgetElement, attrs) {
  if (widgetElement === null) {
    return;
  }
  attrs = attrs || {'data': {}};
  attrs.el = widgetElement;
  m.render(widgetElement, m(window[widgetElement.dataset.widget], attrs));
};

jrvs.truncate = function (s, n) {
  if (s.length > n) {
    return s.substring(0, n) + '...';
  }
  return s;
};

jrvs.widgets = [];

document.addEventListener('DOMContentLoaded', function () {
  jrvs.subscribe();
  // Pre-render widgets until data is available
  jrvs.widgets.forEach(function (name) {
    jrvs.render(jrvs.widgetForJob(name));
  });
});
