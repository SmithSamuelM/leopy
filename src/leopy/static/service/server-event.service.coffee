angular.module "app.lib.devices"
.service "ServerEventSvc", ($log, Actuator, broadcaster, devices, EventSrvc, Sensor, Solution,
                            EVENT_UNLOCKED_ACTUATORS
                            EVENT_ACTUATOR_UPDATE
                            EVENT_SOLUTION_UPDATE
                            EVENT_SENSOR_EVENT)  ->
    self = this
    @debug = false

    @eventsOpened = false

    closeEventStream = () ->
        $log.debug "Closing Event Stream" if self.debug
        EventSrvc.close()
        self.eventsOpened = false

    openEventStream = (callback, tag) ->
        $log.debug "Opening Event Stream" if self.debug
        openPromise = EventSrvc.open {}, callback, tag
        openPromise.then ->
            $log.debug "Success Opening Event Stream" if self.debug
            self.eventsOpened = true
        .catch (data) -> # error method
            $log.debug "Error Opening Event Stream #{data}" if self.debug

        openPromise

    isArray = (object) -> Object.prototype.toString.call(object) is "[object Array]"

    # Receive events from the server,
    # process them here,
    # the use the AngularJS broadcaster to notify interested parts of the code that a change has been made.
    @processEvent = (event) ->
        $log.debug "Event = ", event if self.debug

        if event.tag is EVENT_ACTUATOR_UPDATE
            $log.debug "Event: Actuator Found" if self.debug
            if isArray event.data
                $log.debug ">>>> array data" if self.debug
                for actuator in event.data
                    newActuator = new Actuator actuator
                    $log.debug ">>>> actuator: ", newActuator if self.debug
                    devices.addActuator newActuator
            else
                $log.debug ">>>> single actuator data" if self.debug
                newActuator = new Actuator event.data
                $log.debug ">>>> actuator: ", newActuator if self.debug
                devices.addActuator newActuator

            broadcaster.send event.tag, newActuator
            return

        if event.tag is EVENT_SENSOR_EVENT
            $log.debug "Event: Sensor Found" if self.debug
            if isArray event.data
                $log.debug ">>>> array data" if self.debug
                for actuator in event.data
                    newSensor = new Sensor actuator
                    $log.debug ">>>> actuator: ", newSensor if self.debug
                    devices.addSensor newSensor
            else
                $log.debug ">>>> single actuator data" if self.debug
                newSensor = new Sensor event.data
                $log.debug ">>>> actuator: ", newSensor if self.debug
                devices.addSensor newSensor

            broadcaster.send event.tag, newSensor
            return

        if event.tag is EVENT_SOLUTION_UPDATE
            $log.debug "Event: Solution Found" if self.debug
            if isArray event.data
                $log.debug ">>>> array data" if self.debug
                for actuator in event.data
                    newSolution = new Solution actuator
                    $log.debug ">>>> actuator: ", newSolution if self.debug
                    devices.addSolution newSolution
            else
                $log.debug ">>>> single actuator data" if self.debug
                newSolution = new Solution event.data
                $log.debug ">>>> actuator: ", newSolution if self.debug
                devices.addSolution newSolution

            broadcaster.send event.tag, newSolution
            return

        $log.warn "Unknown event: ", event

    setupEvents = () ->
        closeEventStream()
        openEventStream(self.processEvent)

    setupEvents()

    this
