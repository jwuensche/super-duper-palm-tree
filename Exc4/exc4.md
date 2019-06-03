---
title: Software Defined Networking Exercise 3
author:
  - Fin Christensen
  - Marten Wallewein-Eising
  - Johannes Wünsche
description: Submission for the third exercise of Software Defined Networking
geometry: margin=2cm
---

# SDN Exercise 4


## a) Duties of an SDN Controller

1. Administrating
    1. Setting up VMs on the machine
    2. Handling network failures
2. Monitoring
    1. physical network
    2. vm locations, states
3. Controlling
    1. tunnel setup
    2. rules for packets in virtual and physical network
    3. mapping from virtual to physical network
4. Comminucating with Open vSwitch
    1. transmit flow table
    2. VM placement via a virtual machine manager on the machine OVS is running on (e.g. KVM)

## b) Network Virtualizations with VLANs

> Two datacenters D and E use VLANs for traffic isolation between their hosts. The datacentersare connected over a L3 connection, e.g. the Internet, and need to share their network segments.

### Task I

> Propose a solution (without using SDN or VXLAN) for preserving the slices, even whencommunication is carried out over the L3 link.

Possible solution is wrapping the original packets into another packet then sending this and processing the content on the other side as a incoming
packet of the same network.
In practice this is called encapsulation or tunneling, and just describes exactly this base idea.
Problems can occur that of course before a network can be used additional measures have to be set up and ensured to guarantee functionality, also
monitoring and action in case of network failure may prove more difficult because of this extra layer.

### Task II

> On an example of two hosts A (in Datacenter D) and B (in Datacenter E), draw a communication diagram of a packet sent from A to B over a common network segment. This diagram should include every intermediate hop (except pure L2 switches and simple routers on the Internet).

![diagram1](diagram1.pdf)

### Task III 

> Draw the protocol stack (except Layer 1 and everything above the Transport Layer) of the packet into the diagram, between each two intermediate hops. Example: (Ethernet, IP, UDP)

![diagram2](diagram2.pdf)

\pagebreak

### Task IV
> IV Make yourself familiar with VXLAN and the VXLAN header. Name at least two advantages of VXLAN compared to your solution (Hint: Think about an intermediate NAT between the datacenters).

VXLAN:

- Store L2 information in UDP packets and transfer them over L3 network
- Virtual Extensible LAN Network Identifier (VNI) with 24bits length
- Support of IPSec and TLS
- VXLAN uses VXLAN tunnel endpoint (VTEP) devices to map tenants’ end devices to VXLAN segments and to perform VXLAN encapsulation and de-encapsulation.

Advantages to our solution:

- Supports a huge number of Segements to virtualize traffic
- Easier packet processing using segment ids
- Uses IP-Multicast for Broadcasts, Multicasts and Flooding-Frames

### Task V 
> Name at least one advantage of OpenFlow compared to (pure) VXLAN in the context of network slicing.

Pure VXLAN does not support to assign ports to certain hosts, while with network slicing of OpenFlow multiple ports can be assigned to IPs. 

### c) Energy saving
> Imagine at least one scenario in which SDN can save energy.

- Energy aware routing: Shut down unused paths in the network configuration to save energy
- With increased flexibility of underlying hardware, switches can be optimized for their use cases and become more energy-saving

