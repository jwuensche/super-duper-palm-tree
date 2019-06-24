---
title: Software Defined Networking Exercise 6
author:
  - Fin Christensen
  - Marten Wallewein-Eising
  - Johannes Wünsche
description: Submission for the sixth exercise of Software Defined Networking
geometry: margin=2cm
---

# SDN Exercise 6

## Problem 6.1 - FortNOX

### a) FortNOX Authentication
> How does FortNOX guarantee that only certain users can add/modify/delete flow rules? Which steps are required to be performed by the FortNOX administrator in advance w.r.t. the authentication mechanism.

FortNOX requires source authentication of users that want to add/modify/delete flow rules using digital signatures

- Authorization roles introduced (Operator, Security and Application role
- With Operator role, authorative security policy has to be defined beforehand
- Securit Role can add flow constraints live


### b) FortNOX Rule Conflicts
> How can FortNOX solve rule conflicts? Give an example.

FortNox uses an Alias Set Reduction Algorithm

- Transitive conflicting rules can be detected
- Conflicts arise

Conflict resolution by

- Priority (depending on rule prio)
- Role based priority (who adds the rule)


## Problem 6.2 - SDN Mobile Wireless

### a) Software-Defined MAC Problem
> What is the main conflict between researchers and vendors with respect to Software-Defined MAC?

Problem is: An open programmable platform on NIC is required, but vendors do not want to open their source and to let someone "hack into their NICs"


### b) Solution for previos problem
> Regarding the previous question: What is the most viable approach to solve this problem?

A Protocol that provides enough flexibility resulting in high performance, low cost and a broad range of research, that is consistent with vendors need for closed platforms.

Approaches for this are "Wireless MAC processor" and "MAClets"

### c) Advantages of MAClets
> Name two advantages of MAClets in comparison to traditional MAC stacks.

- New architecture with protocol interpreter that leads to portable code
- Flexibility of used protocols
- Dynamic handling of new features and logics