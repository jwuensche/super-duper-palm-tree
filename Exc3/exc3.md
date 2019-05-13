---
title: Software Defined Networking Exercise 3
author:
  - Fin Christensen
  - Marten Wallewein-Eising
  - Johannes Wünsche
description: Submission for the third exercise of Software Defined Networking
geometry: margin=2cm
---

# SDN Exercise 3

## Problem 3.1 - SDN Relatives to OpenFlow

### a) Concrete SDN implementation

> Name three concrete implementations/instantiations of the SDN concept, other than OpenFlow
> and ForCES.

- OpenContrail: http://www.opencontrail.org/
- VMWare NSX: https://www.vmware.com/de/products/nsx.html
- Floodlight: http://www.projectfloodlight.org/floodlight/
- Big Switch - Big Network Controller: https://searchnetworking.techtarget.com/definition/Big-Switch-Big-Network-Controller

Found in https://www.sciencedirect.com/science/article/pii/S1877050914007327

### b) Forwarding and Control Element Separation

> The Forwarding and Control Element Separation (ForCES) Framework was standardized by the
> IETF in 2004 (RFC 3746). Please revisit the concepts presented in the lecture on ForCES by
> reading Section 1 and 2 of the standard document and answer the following questions. RFC
> 3746: https://tools.ietf.org/html/rfc3746

#### 1) Explain the responsibilities of Control Elememts (CEs) and Forwarding Elements (FEs) in ForCES

Control Elements:
- Give directives to FE how packets have to be forwarded
- Execute control and signal protocols
- Master role in protocol
- Located in control plane

Forwarding Elements:
- Implements packet forwarding as directed by CR
- Slave role in protocol, no FE-FE communication
- Located in data plane 

#### 2) What does the standard state as reason for the separation between FEs and CEs?

- Standardize information exchange between the control and forwarding plane
- Vendors can specialize in one component without having to become experts in all components
- CE and FE from different vendors
- Increased design choices and flexibility for the system vendors
- Enables rapid innovation in both the control and forwarding planes while maintaining interoperability
- Provide better scalability for each separated part instead of scaling both parts

## Problem 3.2 - The OpenFlow Protocol

### a) TCP flag matching - Examples

> OpenFlow v1.5.0 introduces the possibility of TCP flag matching. Name some examples what
> this new feature could be used for and sketch how the solution would work and what other
> OpenFlow features it might require/use.

- Handling urgend packets (URG flag) with higher priority and/or route them to a different route
- Detect beginning (SYN) and end of a TCP connection (FIN), could be used to track the load of a certain conection, this may be used to intially
  create heuristics for incoming connections
- CWR & ECE: Could be used to reschedule the flow of packets if one node experiences currently higher usage
- SYN: DDoS protection if too many TCP connections are tried to be open they may be dropped

### b) Multiple Flow Tables and Pipeline Processing

> Shortly explain the different steps of packet processing inside an OpenFlow Switch with multiple flow tables and in the context of Pipeline Processing

- OpenFlow pipeline consists of two processing types
    - Ingress processing and Egress processing
- Ingress processing:
  + Packet comes to incoming port
  + Defined tables are checked in order and actions are performed in case of table miss and table hit
  + If all tables are checked group actions are performed
  + At the end the defined output actions is performed, if none is defined the paket is dropped
- Egress processing: The same happens for the egress process, for tables with defined outgoing rules
- Both processing types consists of $1$ to $n$ flow tables which define an action set for the processing type

![](matching-flowchart.pdf){ width=60% }

## Problem 3.3 - Flow Spaces

### a) Flow Space Analysis

> Flow spaces can be visualized in a multidimensional space. Fill in the flow spaces corresponding to the given flow rules of the table. Note the number of the corresponding rule next to the corresponding figure.


| Number | Source IP | Destination IP |
| -------- | -------- | -------- |
| 1     | 10.10.2.1      | 10.10.2.1      |
| 2     | 10.10.2.1      | 130.83.1.*     |
| 3     | *              | 192.168.55.76  |
| 4     | 130.83.*       | 130.83.1.*     |



![Flow Space analysis](./flow-space-analysis.pdf)
