---
title: Software Defined Networking Exercise 1
author:
  - Fin Christensen
  - Marten Wallewein-Eising
  - Johannes Wünsche
description: Submission for the first exercise of Software Defined Networking
geometry: margin=2cm
---

# 1.1 Cross-Layer Networking Basics

Alice has a Linux PC. She connects to the Router via Ethernet, and her first action is to "ping"Linus’s PC.

![](sdn11.pdf)

\pagebreak

# 1.2 Routing and Basics

## a) Basic functions of IP, TCP, UDP
 (TODO: Rework)
IP:

- Basis for routing
- Communication over networks

TCP: 

- Access of resources per machine and port
- Provide connection orientation, manage loss and ordering of packets

UPD:

- Access of resources per machine and port

## b) Difference between routing and forwarding
Routing is the information exchange between routers, for example to create and manage a routing table.

Forwarding is making use of the exchanged data to process a packet and to evaluate the next target for the packet.

## c) Link State and Distance Vector routing examples
Link State:

- OSPF: Open Shortest Path First
- IS-IS: Intermediate System to Intermediate System

Distance Vector:

- RIP: Routing Information Protocal
- IGRP: Interior Gateway Routing Protocol

## d) Link State and Distance Vector routing key differences

Link state decides independent on each node based on its own routing table the further path of the packet, every information passed between nodes are about the connection itself.

## e) Most widely used routing protocal between AS
EGP: Exterior Gateway Protocol

## f) MPLS - Multiprotocol Label Switching 

### I What is an "FEC"?

Stands for "Forwarding Equivalence Classes" and describes a set of packets with identical characteristics. Every packet belonging to the same FEC may be handled the same way as every other packet part of it. Labeling an unlabeled incoming packet is the first step in processing them. 


### II Technical motivation of MPLS

MPLS provides the following benefits to use  (TODO: Clarify):

- Reduce effort of looking up entries in huge routing tables
- Support various network protocols, provide a unique interface for them
- Using labels virtual links are possible instead of real endpoints

### III To which layer of IP does MPLS?

- Internet Layer, takes over tasks of routing

# 1.3) SDN

## a) What steps does SDN take to improve the programmability of networks?

The ability of SDN to remote control network hardware, allows for greater freedom for the programmer to adjust existing network structures to demands.
This abstraction also eases the usage of different vendor switches and is not bound by restrictions set by the used hardware.

## b) OpenFlow Behaviour for Firewall Entries

| Switch Port | MAC src | MAC dst | Eth type | VLAN ID | IP src | IP Dst | TCP sport | TCP dport | Action |
|-------------|---------|---------|----------|---------|--------|--------|-----------|-----------|--------|
| `**`        | `**`    | `**`    | `**`     | `**`    | `**`   | `**`   | `**`      | `22`      | `drop` |
OpenFlow would simply check if incoming packets have an incoming TCP port 22, if this is the case they will not be given to the normal switch pipeline, but dropped completely instead. This rule would be given at the beginning or the ending of each lifespan by the network controller to the switches and these act then upon rules(e.g. dropping packets) given by it.

## c) OpenFlow Firewall without involving the network controller

By default is the network controller not included in the packet processing for the given example Firewall entry. As explained above the rules are distributed to the switches and they can be applied without interference, since no dynamic rules are part of the matching process.
