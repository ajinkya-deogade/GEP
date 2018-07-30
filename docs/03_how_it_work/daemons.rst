.. _howitworks/daemons:

===================================
Daemons and how they works together
===================================

Daemons
=======

Alignak framework is made of 6 daemons


Arbiter
-------

The *Arbiter* daemon has several features:

* Load the configuration. In this word configuration, we have:

  * monitoring objects configuration
  * daemons list and configuration (address, port, spare, modules...)

* Manage connections with the other daemons
* Dispatch the configuration to the other daemons

Scheduler
---------

The *Scheduler* manages the checks to run, the period when it needs to run the checks, acknowledge, downtimes...

It is connected to:

* Arbiter
* Poller
* Receiver
* Broker
* Reactionner

Poller
------

The *Poller* runs active checks ordered by *Scheduler*.

It is connected to:

* Arbiter
* Scheduler
* Broker

Receiver
--------

The *Receiver* receives the passive checks

It is connected to:

* Arbiter
* Scheduler
* Broker

Broker
------

The *Broker* gets all events from scheduler

It is connected to:

* Arbiter
* Poller
* Scheduler
* Receiver
* Reactionner


Reactionner
-----------

The *Reactionner* sends the notifications to the users

It is connected to:

* Arbiter
* Scheduler
* Broker
