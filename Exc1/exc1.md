---
title: Software Defined Networking Exercise 1
author:
  - Fin Christensen
  - Marten Wallewein-Eising
  - Johannes Wünsche
description: Submission for the first exercise of Software Defined Networking
geometry: margin=2cm
---

# Cross-Layer Networking Basics

Alice has a Linux PC. She connects to the Router via Ethernet, and her first action is to "ping"Linus’s PC.

![](sdn11.pdf)

# Routing and Basics

## Key Differences between Link State & Distance Vector[

Link state decides independent on each node based on its own routing table the further path of the packet, every information passed between nodes are about the connection itself.

# MPLS

## What is an "FEC"?

Stands for "Forwarding Equivalence Classes", which basically means that every packet belonging to the same FEC are handled the same way as every other packet part of it.

## To which layer of IP does MPLS?

- Internet, takes over tasks of routing

# SDN

## What steps does SDN take to improve the programmability of networks?

The ability of SDN to remote control network hardware, allows for greater freedom for the programmer to adjust existing network structures to demands.
This abstraction also eases the usage of different vendor switches and is not bound by restrictions set by the used hardware.

## OpenFlow Behaviour for Firewall Entries

| Switch Port | MAC src | MAC dst | Eth type | VLAN ID | IP src | IP Dst | TCP sport | TCP dport | Action |
|-------------|---------|---------|----------|---------|--------|--------|-----------|-----------|--------|
| `**`        | `**`    | `**`    | `**`     | `**`    | `**`   | `**`   | `**`      | `22`      | `drop` |
OpenFlow would simply check if incoming packets have an incoming TCP port 22, if this is the case they will not be given to the normal switch pipeline, but dropped completely instead. This rule would be given at the beginning or the ending of each lifespan by the network controller to the switches and these act then upon rules(e.g. dropping packets) given by it.

## OpenFlow Firewall without involving the network controller

By default is the network controller not included in the packet processing for the given example Firewall entry. As explained above the rules are distributed to the switches and they can be applied without interference, since no dynamic rules are part of the matching process.
