# Specification for OpenWRT Remote Manager #

## Rationale ##
This module is intended to be used to manage remote OpenWRT installations that act as network routers. The 
functionality exposed by the module should be a simplified subset of the functionality provided by the Luci web
interface.

## Functional Requirements ##

#### Port Forwarding Management ###
It should provide the capability to
* list all the active port forwarding rules
* delete a specific port forwarding rule
* modify a specific port forwarding rule
* create a new port forwarding rule

#### System User Name and Password Management ####
It should provide the capability to
* change the password of a specific user
* create a new user

#### Network management ####
It should provide the capability to
* retrieve the network information associated with all the available network interfaces
* retrieve the network information associated with a specific available network interface
* set the network information for a specific network interface
* ping an external network location from within the OpenWRT instance

#### Configuration backup ####
It should provide the capability to
* archive and compress the configuration files and respond with the compressed binary tar file

## Non-functional Requirements ##
* Pure Python code only
* Should be usable on Python 2.7

## Architecture ##
At the core of the module there should be an internal abstraction layer responsible for relaying all the RPC messages
back and forth while being presented as regular Python method calls of the exported RPC libraries. 

The actual top-layer functionality provided by the module should be grouped by similarity so as not to clutter the
top-level interface.

### Fault-tolerance ###
Failing operations should never pass silently. Errors should always be propagated as Python exceptions.

## Testing ##
*TODO*
