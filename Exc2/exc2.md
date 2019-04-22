---
title: Software Defined Networking Exercise 2
author:
  - Fin Christensen
  - Marten Wallewein-Eising
  - Johannes Wünsche
description: Submission for the second exercise of Software Defined Networking
geometry: margin=2cm
---

# SDN Exercise 2

## a) Separation of Concerns

> Separation of Concerns: Briefly explain in your own words the different responsibilities of the SDN layers described by Scott Shenker: `Control Program`, `Network Virtualization layer`, and `NOS`.

1. Control Program
    - a program that controls the packet flow in the network based on the abstract network representation (e.g. a graph)
    - provides the data that is needed by the NOS to program the switches
    - implements the configuration of the network
2. Network Virtualization Layer
    - e.g. a graph representation of the network that is managed by the NOS
    - an abstract representation of the network
3. Network Operating System
    - manages all switches in a network and implements the distribution part of a SDN
    - is responsible for the communication of all switches in the network
    - programs the switches
    - creates a global network view

## b) Foundation of Layers

> Foundation of layers: What are the key abstractions that provide the foundation of SDN? Briefly explain what exactly is abstracted, how the interfaces of the abstractions look like, and who uses them.
> Note: This task overlaps with the previous one but requires you to take a more conceptual perspective.

1. Distributed State Abstraction
    - distributed state is the state (tables) on the switches
    - by abstracting the global state a global network view over all switches in the distributed network is created
    - communicates with the switches
2. Specification Abstraction
    - control program defines the behavior of the switches in the network based on the distributed state abstraction (e.g. a graph)
    - does not care about the physical implementation in the network
3. Forwarding Abstraction
    - defines how the specification of the network is implemented on the switches
    - the implementation of the control plane
    - independent of the forwarding-hardware
    - a flexible model to define the forwarding rules created by the control program

## c) Scale-Out Router

> Briefly explain the concept of a “scale-out router” in the context of network virtualization (slide 42, lecture 2). What is the advantage of using this abstraction in the context of the above discussed abstractions?

1. Scaling Up
    - increasing capacity of a single router
    - just make it bigger to handle more load
2. Scale out
    - distribute load over multiple systems
    - requires abstraction for the system to let multiple devices act like a single instance
    - an abstract view is created which represents a single router
    - physically multiple devices are interconnected
    - load is balanced between the interconnected devices
    - the more abstraction there is, the better the distribution of the load
        - when the control program is a software, it can be run on normal servers
        - for normal servers there are techniques to distribute computation load over multiple servers (cloud computation)

## d) Single Point of Failure

> When network engineers start learning about SDN, they often get the impression that the concept introduces a single point of failure to the process of network control. Why is this the case and why is it not true after what you learned in the first lectures? Please briefly explain.

The central control server is needed to calculate a route for a packet through the network. When this control server is offline, no routes can be calculated. However, as most packets (~90%) are of the same type as other packets that were routed earlier, the switches are using the previously programmed route for the packet type. This means that only new routes cannot be calculated when the central control server goes offline.
